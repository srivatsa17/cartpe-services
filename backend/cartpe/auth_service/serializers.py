from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from auth_service.models import User
from auth_service.token import account_activation_token

MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_LENGTH = 70

class RegisterUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(min_length = 2, max_length = 255)
    last_name = serializers.CharField(min_length = 2, max_length = 255)
    email = serializers.EmailField(min_length = 3, max_length = 255, allow_blank = False)
    password = serializers.CharField(min_length = MIN_PASSWORD_LENGTH, max_length = MAX_PASSWORD_LENGTH, write_only = True)

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
    email = serializers.EmailField(min_length = 3, max_length = 255, allow_blank = False)
    password = serializers.CharField(min_length = MIN_PASSWORD_LENGTH, max_length = MAX_PASSWORD_LENGTH, write_only = True)

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        # authenticate() checks for user.is_active field as well.
        # If user.is_active is False, authenticate method returns None, denying the login for inactive users.
        user = authenticate(email = email, password = password)

        if not user:
            raise AuthenticationFailed(
                "Please ensure that your credentials are valid and that the user account is enabled."
            )

        if not user.is_verified:
            raise AuthenticationFailed("Please ensure that your email is verified.")

        return user

    def to_representation(self, instance):
        return {
            'email': instance.email,
            'firstName': instance.first_name,
            'lastName': instance.last_name,
            'tokens': instance.tokens
        }

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    class Meta:
        fields = ['refresh_token']

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(min_length = MIN_PASSWORD_LENGTH, max_length = MAX_PASSWORD_LENGTH, write_only = True)
    new_password = serializers.CharField(min_length = MIN_PASSWORD_LENGTH, max_length = MAX_PASSWORD_LENGTH, write_only = True)
    confirm_new_password = serializers.CharField(min_length = MIN_PASSWORD_LENGTH, max_length = MAX_PASSWORD_LENGTH, write_only = True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'confirm_new_password']

    def containsLetterAndNumber(self, input):
        return input.isalnum() and not input.isalpha() and not input.isdigit()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context.get('user', '')
        old_password = attrs.get('old_password', '')
        new_password = attrs.get('new_password', '')
        confirm_new_password = attrs.get('confirm_new_password', '')

        if not user.check_password(old_password):
            raise ValidationError("Old password is incorrect.")

        if old_password == new_password:
            raise ValidationError("New password is same as Old password.")

        if not self.containsLetterAndNumber(new_password):
            raise ValidationError("Password should contain alphabets and digits.")

        if new_password != confirm_new_password:
            raise ValidationError("New passwords not matching.")

        return attrs

class DeactivateAccountSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    class Meta:
        fields = ['refresh_token']