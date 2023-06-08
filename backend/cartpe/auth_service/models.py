from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, password):
        if email is None:
            raise TypeError('Email should not be empty')

        if password is None:
            raise TypeError('Password should not be empty')

        user = self.model(email = self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError('Password should not be empty')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    MALE, FEMALE, OTHERS = "Male", "Female", "Other"
    GENDER_CHOICES = [
        (MALE, "MALE"), (FEMALE, "FEMALE"), (OTHERS, "OTHERS")
    ]

    email = models.EmailField(max_length = 255, unique = True, db_index = True, null = False, blank = False)
    first_name = models.CharField(max_length = 255, null = True, blank = True)
    last_name = models.CharField(max_length = 255, null = True, blank = True)
    is_verified = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    profile_picture = models.ImageField(max_length = 255, null = True, blank = True)
    gender = models.CharField(max_length = 10, choices = GENDER_CHOICES, null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def tokens(self):
        token = RefreshToken.for_user(self)
        return {
            'refresh': str(token),  # By default gives the refresh token
            'access': str(token.access_token)
        }