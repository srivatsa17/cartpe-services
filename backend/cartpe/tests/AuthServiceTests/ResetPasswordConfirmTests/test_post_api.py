from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from auth_service.models import User

# Global variables
CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()


class ResetPasswordConfirmTest(APITestCase):
    """Test module for POST request for ResetPasswordConfirmAPIView API"""

    def get_url(self):
        url = reverse("reset-password-confirm")
        return url

    def setUp(self):
        self.user = User.objects.create(email="testuser@example.com", password="abcdefgh")

    def test_success(self):
        url = self.get_url()
        data = json.dumps(
            {
                "new_password": "testuser123",
                "confirm_new_password": "testuser123",
                "uid": urlsafe_base64_encode(force_bytes(self.user.pk)),
                "token": default_token_generator.make_token(self.user),
            }
        )

        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual("Password reset successful.", response.data["message"])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_with_non_alphanumeric_passwords(self):
        url = self.get_url()
        data = json.dumps(
            {
                "new_password": "testuser",
                "confirm_new_password": "testuser",
                "uid": urlsafe_base64_encode(force_bytes(self.user.pk)),
                "token": default_token_generator.make_token(self.user),
            }
        )

        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(
            "Password should contain alphabets and digits.", response.data["message"][0]
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_with_unmatched_passwords(self):
        url = self.get_url()
        data = json.dumps(
            {
                "new_password": "testuser1234",
                "confirm_new_password": "testuser123",
                "uid": urlsafe_base64_encode(force_bytes(self.user.pk)),
                "token": default_token_generator.make_token(self.user),
            }
        )

        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual("New passwords not matching.", response.data["message"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_with_invalid_uid(self):
        url = self.get_url()
        data = json.dumps(
            {
                "new_password": "testuser123",
                "confirm_new_password": "testuser123",
                "uid": "abcd123",
                "token": default_token_generator.make_token(self.user),
            }
        )

        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(
            "Error occurred while decoding base64 user id", response.data["message"][0]
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_with_invalid_decoded_pk(self):
        url = self.get_url()
        data = json.dumps(
            {
                "new_password": "testuser123",
                "confirm_new_password": "testuser123",
                "uid": urlsafe_base64_encode(force_bytes(self.user.pk)) + "a",
                "token": default_token_generator.make_token(self.user),
            }
        )

        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual("Invalid type received for user id", response.data["message"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_with_non_existing_user(self):
        url = self.get_url()
        data = json.dumps(
            {
                "new_password": "testuser123",
                "confirm_new_password": "testuser123",
                "uid": urlsafe_base64_encode(force_bytes(123)),
                "token": default_token_generator.make_token(self.user),
            }
        )

        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual("Unable to find user", response.data["message"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_with_invalid_token(self):
        url = self.get_url()
        data = json.dumps(
            {
                "new_password": "testuser123",
                "confirm_new_password": "testuser123",
                "uid": urlsafe_base64_encode(force_bytes(self.user.pk)),
                "token": "invalid_token",
            }
        )

        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual("Invalid or expired token", response.data["message"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
