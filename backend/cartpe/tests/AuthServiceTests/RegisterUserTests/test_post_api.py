from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from auth_service.models import User

# Global variables
CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()

class PostRegisterUserTest(APITestCase):
    """ Test module for POST request for RegisterAPIView API """

    def get_url(self):
        url = reverse("register")
        return url

    def setUp(self):
        self.valid_data = {
            "email" : "testuser@example.com",
            "password" : "testpassword",
            "first_name": "testuser",
            "last_name": "testuser"
        }
        self.invalid_data = { "email" : "abc", "password" : "abc" }

    @patch("auth_service.views.send_verification_email_task.delay")
    def test_register_with_valid_data(self, mock_send_verification_email_task):
        url = self.get_url()
        data = json.dumps(self.valid_data)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        # Assert that the send_verification_email function was called with the correct email
        mock_send_verification_email_task.assert_called_once_with(user_email=self.valid_data["email"])

    @patch("auth_service.views.send_verification_email_task.delay")
    def test_register_with_invalid_data(self, mock_send_verification_email_task):
        url = self.get_url()
        data = json.dumps(self.invalid_data)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        mock_send_verification_email_task.assert_not_called()

    @patch("auth_service.views.send_verification_email_task.delay")
    def test_register_with_existing_email(self, mock_send_verification_email_task):
        User.objects.create(email = self.valid_data["email"], password = "abcdefgh")

        url = self.get_url()
        data = json.dumps(self.valid_data)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        mock_send_verification_email_task.assert_not_called()