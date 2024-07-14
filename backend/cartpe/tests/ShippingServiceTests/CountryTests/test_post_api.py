from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from auth_service.models import User

CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()


class PostCountryTest(APITestCase):
    """Test module for POST request for BrandAPIView API"""

    def get_url(self):
        url = reverse("country")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        self.valid_data = {"name": "India"}

    def test_post_with_valid_data(self):
        url = self.get_url()
        data = json.dumps(self.valid_data)
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post_with_missing_fields(self):
        url = self.get_url()
        data = json.dumps({})
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual("This field is required.", response.data["name"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_with_same_name(self):
        url = self.get_url()
        data = json.dumps(self.valid_data)
        client.post(url, data=data, content_type=CONTENT_TYPE)
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(
            "Country '%s' already exists and cannot be created again." % self.valid_data["name"],
            response.data["message"][0],
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
