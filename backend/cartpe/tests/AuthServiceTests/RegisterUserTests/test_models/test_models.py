from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from auth_service.models import User

class AuthUserModelTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email = "abc@gmail.com", password = "abcdef")

    def test_str_is_equal_to_email(self):
        expectedResponse = self.user.email
        receivedResponse = str(self.user)

        self.assertEqual(receivedResponse, expectedResponse)

    def test_with_None_Type_email(self) -> None:
        with self.assertRaises(ValidationError):
            User.objects.create_user(email = None, password = "abcdef")

    def test_with_None_Type_password(self) -> None:
        with self.assertRaises(ValidationError):
            User.objects.create_user(email = "abc@gmail.com", password = None)

        with self.assertRaises(ValidationError):
            User.objects.create_superuser(email = "abc@gmail.com", password = None)

    def test_create_super_user(self) -> None:
        user = User.objects.create_superuser(email = "abcd@gmail.com", password = "abcdef")

        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)