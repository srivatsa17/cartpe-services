from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from auth_service.models import User

# Initialize the APIClient app
client = APIClient()

# Global variables
CONTENT_TYPE = "application/json"


class EditProfileTests(APITestCase):
    """Test module for PATCH request to EditProfileAPIView api"""

    def get_url(self):
        url = reverse("edit-profile")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

    def test_success(self):
        url = self.get_url()

        # Making sure entries are there in User model
        data = json.dumps({"gender": "Male", "phone": "1234567890", "date_of_birth": "1999-05-11"})
        client.patch(url, data=data, content_type=CONTENT_TYPE)

        response = client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data)
        self.assertEqual("Male", response.data["gender"])
        self.assertEqual("1234567890", response.data["phone"])
        self.assertEqual("1999-05-11", response.data["date_of_birth"])
