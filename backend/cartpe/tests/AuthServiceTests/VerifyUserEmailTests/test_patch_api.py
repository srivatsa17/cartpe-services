from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from auth_service.models import User
from auth_service.token import account_activation_token

# Global variables
CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()

class VerifyUserEmailTest(APITestCase):
    """ Test module for PATCH request for VerifyUserEmailAPIView API """

    def get_url(self):
        url = reverse("verify-email")
        return url

    def setUp(self):
        self.user = User.objects.create(email = "testuser@example.com", password = "abcdefgh")

    def test_verify_email_success(self):
        url = self.get_url()
        data = json.dumps({
            "uid" : urlsafe_base64_encode(force_bytes(self.user.pk)),
            "token" : account_activation_token.make_token(self.user)
        })

        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertTrue(response.data["isEmailVerified"])
        self.assertEqual("Email Verified Successfully", response.data["message"])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_verify_email_invalid_uid(self):
        url = self.get_url()
        data = json.dumps({
            "uid" : "abcd123",
            "token" : account_activation_token.make_token(self.user)
        })

        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("Error occurred while decoding base64 user id", response.data["message"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_verify_email_invalid_decoded_pk(self):
        url = self.get_url()
        data = json.dumps({
            "uid" : urlsafe_base64_encode(force_bytes(self.user.pk)) + "a",
            "token" : account_activation_token.make_token(self.user)
        })

        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("Invalid type received for user id",response.data["message"][0] )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_verify_email_non_existing_user(self):
        url = self.get_url()
        data = json.dumps({
            "uid" : urlsafe_base64_encode(force_bytes(123)),
            "token" : account_activation_token.make_token(self.user)
        })

        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("Unable to find user", response.data["message"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_verify_email_invalid_token(self):
        url = self.get_url()
        data = json.dumps({
            "uid" : urlsafe_base64_encode(force_bytes(self.user.pk)),
            "token" : "invalid_token"
        })

        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("Invalid or expired token", response.data["message"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)