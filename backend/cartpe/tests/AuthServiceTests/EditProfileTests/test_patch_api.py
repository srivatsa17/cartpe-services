from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from auth_service.models import User

# Global variables
CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()

class EditProfileTests(APITestCase):
    """ Test module for PATCH request to EditProfileAPIView api """

    def get_url(self):
        url = reverse("edit-profile")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

    def test_success(self):
        url = self.get_url()
        data = json.dumps({
            "gender": "Male",
            "phone": "1234567890",
            "date_of_birth" : "1999-05-11"
        })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data)

    def test_email_edit_failure(self):
        url = self.get_url()
        data = json.dumps({
            "email": "abc@gmail.com"
        })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual("Email cannot be updated.", str(response.data["message"][0]))
