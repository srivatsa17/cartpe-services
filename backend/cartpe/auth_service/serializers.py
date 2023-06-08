from rest_framework import serializers
from auth_service.models import User

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