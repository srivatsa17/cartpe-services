from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from auth_service.models import User

# Global variables
CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()

class ChangePasswordTests(APITestCase):
    """ Test module for PATCH request to ChangePasswordAPIView api """

    def get_url(self):
        url = reverse("change-password")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

    def test_change_password_success(self):
        url = self.get_url()
        data = json.dumps({
            "old_password" : "abcdef",
            "new_password" : "testuser123",
            "confirm_new_password" : "testuser123"
        })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("Password updated successfully.", response.data["message"])

    def test_change_password_with_empty_body(self):
        url = self.get_url()
        data = json.dumps({})
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(status.HTTP_400_BAD_REQUEST, receivedStatusCode)
        self.assertEqual("This field is required.", response.data["old_password"][0])
        self.assertEqual("This field is required.", response.data["new_password"][0])
        self.assertEqual("This field is required.", response.data["confirm_new_password"][0])

    def test_change_password_with_wrong_old_password(self):
        url = self.get_url()
        data = json.dumps({
            "old_password" : "abcdefg",
            "new_password" : "testuser123",
            "confirm_new_password" : "testuser123"
        })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual("Old password is incorrect.", response.data["message"][0])

    def test_change_password_with_same_password(self):
        url = self.get_url()
        data = json.dumps({
            "old_password" : "abcdef",
            "new_password" : "abcdef",
            "confirm_new_password" : "abcdef"
        })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual("New password is same as Old password.", response.data["message"][0])

    def test_change_password_with_no_alphanumeric_chars(self):
        url = self.get_url()
        data = json.dumps({
            "old_password" : "abcdef",
            "new_password" : "testuser",
            "confirm_new_password" : "testuser"
        })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual("Password should contain alphabets and digits.", response.data["message"][0])

    def test_change_password_with_unmatched_new_passwords(self):
        url = self.get_url()
        data = json.dumps({
            "old_password" : "abcdef",
            "new_password" : "testuser123",
            "confirm_new_password" : "testuser12"
        })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual("New passwords not matching.", response.data["message"][0])