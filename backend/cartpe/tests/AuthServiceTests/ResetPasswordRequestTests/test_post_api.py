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


class PostResetPasswordRequestTest(APITestCase):
    """Test module for POST request for ResetPasswordRequestAPIView API"""

    def get_url(self):
        url = reverse("reset-password")
        return url

    def setUp(self):
        self.valid_data = {"email": "testuser@example.com"}
        self.invalid_data = {"email": "abc"}

    @patch("auth_service.views.send_reset_password_email_task.delay")
    def test_with_valid_data(self, mock_send_reset_password_email_task):
        User.objects.create_user(email="testuser@example.com", password="test@123")

        url = self.get_url()
        data = json.dumps(self.valid_data)
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Assert that the send_reset_password_email function was called with the correct email
        mock_send_reset_password_email_task.assert_called_once_with(
            user_email=self.valid_data["email"]
        )

    @patch("auth_service.views.send_reset_password_email_task.delay")
    def test_with_invalid_data(self, mock_send_reset_password_email_task):
        url = self.get_url()
        data = json.dumps(self.invalid_data)
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        mock_send_reset_password_email_task.assert_not_called()

    @patch("auth_service.views.send_reset_password_email_task.delay")
    def test_with_non_existing_user(self, mock_send_reset_password_email_task):
        url = self.get_url()
        data = json.dumps(self.valid_data)
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual("Email does not exist.", str(response.data["message"][0]))
        mock_send_reset_password_email_task.assert_not_called()
