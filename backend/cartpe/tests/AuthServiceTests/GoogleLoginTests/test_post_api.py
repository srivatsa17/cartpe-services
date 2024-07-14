from unittest import mock
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from auth_service.models import User
import json

# Global variables
CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()


class GoogleLoginAPITestCase(APITestCase):
    """Test module for POST request for GoogleLoginAPIView API"""

    def get_url(self):
        url = reverse("google-login")
        return url

    def setUp(self):
        self.mocked_token_response = {
            "access_token": "mocked_access_token",
            "expires_in": 3599,
            "token_type": "Bearer",
            "scope": "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email",
            "refresh_token": "mocked_refresh_token",
        }
        self.mocked_user_info = {
            "id": "1234567890",
            "email": "testuser@example.com",
            "verified_email": True,
            "name": "Test User",
            "given_name": "Test",
            "family_name": "User",
            "picture": "http://example.com/picture.jpg",
            "locale": "en",
        }

    @mock.patch("requests.post")
    @mock.patch("requests.get")
    def test_success_with_existing_user(self, mock_get, mock_post):
        self.user = User.objects.create(
            email=self.mocked_user_info["email"],
            password="abcdef",
            first_name=self.mocked_user_info["given_name"],
            last_name=self.mocked_user_info["family_name"],
        )

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = self.mocked_token_response

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.mocked_user_info

        data = json.dumps({"code": "mocked_authorization_code"})

        url = self.get_url()
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.mocked_user_info["email"], response.data["email"])
        self.assertEqual(self.mocked_user_info["given_name"], response.data["first_name"])
        self.assertEqual(self.mocked_user_info["family_name"], response.data["last_name"])

    @mock.patch("requests.post")
    @mock.patch("requests.get")
    def test_success_with_non_existing_user(self, mock_get, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = self.mocked_token_response

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.mocked_user_info

        data = json.dumps({"code": "mocked_authorization_code"})

        url = self.get_url()
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.mocked_user_info["email"], response.data["email"])
        self.assertEqual(self.mocked_user_info["given_name"], response.data["first_name"])
        self.assertEqual(self.mocked_user_info["family_name"], response.data["last_name"])

    @mock.patch("requests.post")
    @mock.patch("requests.get")
    def test_failure_with_inactive_user(self, mock_get, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = self.mocked_token_response

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.mocked_user_info

        self.user = User.objects.create(
            email=self.mocked_user_info["email"],
            password="abcdef",
            first_name=self.mocked_user_info["given_name"],
            last_name=self.mocked_user_info["family_name"],
        )

        # Set user's is_active state to false
        self.user.is_active = False
        self.user.save()

        data = json.dumps({"code": "mocked_authorization_code"})

        url = self.get_url()
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual("User account is not active.", str(response.data["detail"]))

    @mock.patch("requests.post")
    def test_failure_with_no_code(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = "This field is required."

        data = json.dumps({})

        url = self.get_url()
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual("This field is required.", str(response.data["code"][0]))

    @mock.patch("requests.post")
    def test_with_not_ok_response_from_access_token_url(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.ok = False
        mock_post.return_value.json.return_value = {"error": "invalid_grant"}

        data = json.dumps({"code": "mocked_authorization_code"})

        url = self.get_url()
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual("invalid_grant", str(response.data["error"][0]))

    @mock.patch("requests.post")
    def test_with_no_access_token_from_access_token_url(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.ok = True
        # Delete the access_token key from dict to simulate scenario of no access_token.
        del self.mocked_token_response["access_token"]
        mock_post.return_value.json.return_value = self.mocked_token_response

        data = json.dumps({"code": "mocked_authorization_code"})

        url = self.get_url()
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            "Unable to fetch access token from Google response.", str(response.data["message"][0])
        )

    @mock.patch("requests.post")
    @mock.patch("requests.get")
    def test_with_no_access_token_to_user_info_url(self, mock_get, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = self.mocked_token_response

        mock_get.return_value.status_code = 400
        # Make the access_token to None to simulate scenario.
        self.mocked_token_response["access_token"] = None
        mock_get.return_value.json.return_value = "Field access_token is required."

        data = json.dumps({"code": "mocked_authorization_code"})

        url = self.get_url()
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual("Field access_token is required.", str(response.data["message"][0]))

    @mock.patch("requests.post")
    @mock.patch("requests.get")
    def test_with_not_ok_response_from_user_info_url(self, mock_get, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = self.mocked_token_response

        mock_get.return_value.status_code = 400
        mock_get.return_value.ok = False
        mock_get.return_value.json.return_value = "Failed to obtain user info from Google."

        data = json.dumps({"code": "mocked_authorization_code"})

        url = self.get_url()
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            "Failed to obtain user info from Google.", str(response.data["message"][0])
        )
