from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from auth_service.models import User
from auth_service.token import account_activation_token
from auth_service.utils import google_api_client
from cartpe import settings
import re

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 70

class RegisterUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(min_length = 2, max_length = 255)
    last_name = serializers.CharField(min_length = 2, max_length = 255)
    email = serializers.EmailField(min_length = 3, max_length = 255, allow_blank = False)
    password = serializers.CharField(min_length = MIN_PASSWORD_LENGTH, max_length = MAX_PASSWORD_LENGTH, write_only = True)

    class Meta:
        model = User
        fields = [
            "id", "email", "first_name", "last_name", "password", "is_verified", "is_active", "is_staff",
            "created_at", "updated_at"
        ]
        read_only_fields = [
            "first_name", "last_name", "is_verified", "is_active", "is_staff", "created_at", "updated_at"
        ]

    def validate(self, attrs):
        email = attrs.get("email", "")

        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError({
                "message": "A user with same email-id already exists"
            })
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class GoogleRegisterSerializer(serializers.Serializer):
    code = serializers.CharField()

    class Meta:
        fields = ["code"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        code = attrs.get("code", "")

        redirect_uri = f"{settings.BASE_FRONTEND_URL}/user/register/google"
        access_token = google_api_client.get_google_access_token(code=code, redirect_uri=redirect_uri)
        user_data = google_api_client.get_google_user_info(access_token=access_token)

        if User.objects.filter(email = user_data["email"]).exists():
            raise ValidationError({
                "message": "A user with same email-id already exists"
            })

        user = User.objects.create(
            email = user_data.get("email", ""),
            first_name = user_data.get("given_name", ""),
            last_name = user_data.get("family_name", ""),
            is_verified = user_data.get("email_verified", False),
            is_active = True
        )

        data = {
            "email" : user.email,
            "first_name": user.first_name,
            "last_name": user.last_name or None,
            "tokens": user.tokens
        }

        return data

class EmailVerificationSerializer(serializers.Serializer):
    uid = serializers.CharField(min_length = 1, max_length = 20)
    token = serializers.CharField(min_length = 10, max_length = 100)

    class Meta:
        fields = ["uid", "token"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        uid = attrs.get("uid", "")
        token = attrs.get("token", "")

        try:
            pk = urlsafe_base64_decode(uid).decode()
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
        fields = ["email", "first_name", "last_name", "password", "tokens"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        # authenticate() checks for user.is_active field as well.
        # If user.is_active is False, authenticate method returns None, denying the login for inactive users.
        user = authenticate(email = email, password = password)

        if not user:
            raise AuthenticationFailed(
                "Please ensure that your credentials are valid and that the user account is active."
            )

        if not user.is_verified:
            raise AuthenticationFailed("Please ensure that your email is verified.")

        return user

class GoogleLoginSerializer(serializers.Serializer):
    code = serializers.CharField()

    class Meta:
        fields = ["code"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        code = attrs.get("code", "")

        redirect_uri = f"{settings.BASE_FRONTEND_URL}/user/login/google"
        access_token = google_api_client.get_google_access_token(code=code, redirect_uri=redirect_uri)
        user_data = google_api_client.get_google_user_info(access_token=access_token)
        user = None

        try:
            user = User.objects.get(email=user_data["email"])

            if not user.is_active:
                raise AuthenticationFailed("User account is not active.")

        except User.DoesNotExist:
            user = User.objects.create(
                email = user_data.get("email", ""),
                first_name = user_data.get("given_name", ""),
                last_name = user_data.get("family_name", ""),
                is_verified = user_data.get("email_verified", False),
                is_active = True
            )

        data = {
            "email" : user.email,
            "first_name": user.first_name,
            "last_name": user.last_name or None,
            "tokens": user.tokens
        }

        return data

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    class Meta:
        fields = ["refresh_token"]

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(min_length = MIN_PASSWORD_LENGTH, max_length = MAX_PASSWORD_LENGTH, write_only = True)
    new_password = serializers.CharField(min_length = MIN_PASSWORD_LENGTH, max_length = MAX_PASSWORD_LENGTH, write_only = True)
    confirm_new_password = serializers.CharField(min_length = MIN_PASSWORD_LENGTH, max_length = MAX_PASSWORD_LENGTH, write_only = True)

    class Meta:
        model = User
        fields = ["old_password", "new_password", "confirm_new_password"]

    def containsAlphaAndDigits(self, input):
        # Regular expression to match at least one alphabet and one digit
        pattern = r'(?=.*[a-zA-Z])(?=.*\d)'
        return bool(re.search(pattern, input))

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context.get("user", "")
        old_password = attrs.get("old_password", "")
        new_password = attrs.get("new_password", "")
        confirm_new_password = attrs.get("confirm_new_password", "")

        if not user.check_password(old_password):
            raise ValidationError("Old password is incorrect.")

        if old_password == new_password:
            raise ValidationError("New password is same as Old password.")

        if not self.containsAlphaAndDigits(new_password):
            raise ValidationError("Password should contain alphabets and digits.")

        if new_password != confirm_new_password:
            raise ValidationError("New passwords not matching.")

        return attrs

class DeactivateAccountSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    class Meta:
        fields = ["refresh_token"]

class EditProfileSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")
    updated_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")

    class Meta:
        model = User
        fields = [
            "id", "email", "first_name", "last_name", "gender", "phone", "date_of_birth",
            "created_at", "updated_at"
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        email = attrs.get("email", "")

        if len(email):
            raise ValidationError({
                "message": "Email cannot be updated."
            })

        return attrs