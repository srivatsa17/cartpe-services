from unittest.mock import MagicMock, patch
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from auth_service.models import User

# Global variables
CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()


class PostLogoutUserTests(APITestCase):
    """Test module for POST request for LogoutAPIView api"""

    def get_url(self):
        url = reverse("logout")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

    @patch("auth_service.views.RefreshToken")
    def test_logout_success(self, mock_for_user):
        mock_refresh_token = MagicMock()
        mock_for_user.return_value = mock_refresh_token

        url = self.get_url()
        data = json.dumps({"refresh_token": "mock_refresh_token"})
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertIsNone(response.data)

    def test_logout_with_no_body(self):
        url = self.get_url()
        data = json.dumps({})
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
