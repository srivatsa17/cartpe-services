from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from auth_service.models import User

# Global variables
CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()


class ContactUsAPITestCase(APITestCase):
    """Test module to create an inquiry to ContactUsAPIView API"""

    def get_url(self):
        url = reverse("contact_us")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

    def test_create_inquiry_success(self):
        url = self.get_url()
        data = json.dumps({"topic": "Order Status", "comment": "I have a problem with order #120."})
        response = client.post(url, data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIsNotNone(response.data)

    def test_create_inquiry_failure(self):
        url = self.get_url()
        data = json.dumps({"topic": "Order Status", "comment": ""})
        response = client.post(url, data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIsNotNone("This field is required.", str(response.data["comment"][0]))
