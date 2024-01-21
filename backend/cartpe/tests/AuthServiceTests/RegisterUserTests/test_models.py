from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from auth_service.models import User

class AuthUserModelTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email = "abc@gmail.com", password = "abcdef")

    def test_str_is_equal_to_email(self):
        self.assertEqual(self.user.email, str(self.user))

    def test_with_none_type_email(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(email = None, password = "abcdef")

    def test_with_none_type_password(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(email = "abc@gmail.com", password = None)

        with self.assertRaises(ValidationError):
            User.objects.create_superuser(email = "abc@gmail.com", password = None)

    def test_create_super_user(self):
        user = User.objects.create_superuser(email = "abcd@gmail.com", password = "abcdef")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)