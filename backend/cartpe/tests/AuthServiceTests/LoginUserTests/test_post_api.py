from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from auth_service.models import User

# Global variables
CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()


class PostLoginUserTest(APITestCase):
    """Test module for POST request for LoginAPIView API"""

    def get_url(self):
        url = reverse("login")
        return url

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="test@123",
            first_name="testuser",
            last_name="testuser",
        )

    def test_login_success(self):
        url = self.get_url()
        data = json.dumps({"email": "testuser@example.com", "password": "test@123"})
        self.user.is_verified = True
        self.user.save()

        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data)

    def test_login_with_empty_username_password(self):
        url = self.get_url()
        data = json.dumps({"email": "", "password": ""})

        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual("This field may not be blank.", response.data["email"][0])
        self.assertTrue("This field may not be blank.", response.data["password"][0])

    def test_login_with_non_existing_user(self):
        url = self.get_url()
        data = json.dumps({"email": "nonexistinguser@example.com", "password": "test@123"})
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(
            "Please ensure that your credentials are valid and that the user account is active.",
            response.data["detail"],
        )

    def test_login_with_invalid_credentials(self):
        url = self.get_url()
        data = json.dumps({"email": "testuser@example.com", "password": "test@1234"})
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(
            "Please ensure that your credentials are valid and that the user account is active.",
            response.data["detail"],
        )

    def test_login_with_non_verified_user(self):
        url = self.get_url()
        data = json.dumps({"email": "testuser@example.com", "password": "test@123"})

        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual("Please ensure that your email is verified.", response.data["detail"])
