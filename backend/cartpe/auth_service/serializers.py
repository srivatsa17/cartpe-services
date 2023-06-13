from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from auth_service.models import User
from auth_service.token import account_activation_token

class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length = 3, max_length = 255, allow_blank = False)
    password = serializers.CharField(min_length = 6, max_length = 68, write_only = True, trim_whitespace = True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'password', 'is_verified', 'is_active', 'is_staff', 'profile_picture',
            'gender', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'first_name', 'last_name', 'is_verified', 'is_active', 'is_staff', 'profile_picture', 'gender', 'created_at',
            'updated_at'
        ]

    def validate(self, attrs):
        email = attrs.get('email', '')

        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError({
                "message": "A user with same email-id already exists"
            })
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class EmailVerificationSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(min_length = 1, max_length = 20)
    token = serializers.CharField(min_length = 10, max_length = 100)

    class Meta:
        fields = ['uidb64', 'token']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        uidb64 = attrs.get('uidb64', '')
        token = attrs.get('token', '')

        try:
            pk = urlsafe_base64_decode(uidb64).decode()
        except Exception:
            raise ValidationError("Error occurred while decoding base64 user id")
        
        if not pk.isnumeric():
            raise ValidationError("Invalid type received for user id")

        if not User.objects.filter(pk = pk).exists():
            raise ValidationError("Unable to find user")

        user = User.objects.get(pk = pk)
        isTokenValid = account_activation_token.check_token(user, token)

        if not isTokenValid:
            raise ValidationError("Invalid or expired token")

        return user
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length = 3, max_length = 255, write_only = True, allow_blank = False)
    password = serializers.CharField(min_length = 6, max_length = 68, write_only = True, trim_whitespace = True)

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = authenticate(email = email, password = password)

        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")
        
        if not user.is_active:
            raise AuthenticationFailed("Account disabled")

        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        return {
            'tokens' : user.tokens
        }