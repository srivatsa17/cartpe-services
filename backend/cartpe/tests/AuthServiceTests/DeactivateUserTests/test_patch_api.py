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


class DeactivateAccountTests(APITestCase):
    """Test module for PATCH request to DeactivateAccountAPIView api"""

    def get_url(self):
        url = reverse("deactivate")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

    @patch("auth_service.views.RefreshToken")
    def test_deactivate_user_account_success(self, mock_for_user):
        mock_refresh_token = MagicMock()
        mock_for_user.return_value = mock_refresh_token

        url = self.get_url()
        data = json.dumps({"refresh_token": "mocked_refresh_token"})
        response = client.patch(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("Account deactivated successfully.", response.data["message"])

    def test_deactivate_user_account_failure(self):
        url = self.get_url()
        data = json.dumps({})
        response = client.patch(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
