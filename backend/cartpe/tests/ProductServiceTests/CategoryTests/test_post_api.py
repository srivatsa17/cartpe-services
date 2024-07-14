from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from auth_service.models import User

# Global variables
CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()


class PostCategoryTest(APITestCase):
    """Test module for POST request for CategoryAPIView API"""

    def get_url(self):
        url = reverse("categories")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        self.valid_data = {"name": "Men", "description": "Clothing for men", "parent": None}
        self.subcategory = {"name": "Topwear", "description": "Topwear for men", "parent": "Men"}

    def test_post_with_valid_data(self):
        url = self.get_url()
        data = json.dumps(self.valid_data)
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIsNotNone(response.data)

    def test_post_with_subcategory(self):
        url = self.get_url()
        data = json.dumps(self.subcategory)
        client.post(url, data=json.dumps(self.valid_data), content_type=CONTENT_TYPE)
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIsNotNone(response.data)

    def test_post_with_missing_fields(self):
        url = self.get_url()
        data = json.dumps({})
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual("This field is required.", response.data["name"][0])
        self.assertEqual("This field is required.", response.data["description"][0])
        self.assertEqual("This field is required.", response.data["parent"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_with_non_existing_parent(self):
        url = self.get_url()
        data = json.dumps(self.subcategory)
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual("Object with name=Men does not exist.", response.data["parent"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_with_same_name_and_parent_combination(self):
        url = self.get_url()
        data = json.dumps(self.valid_data)
        client.post(url, data=data, content_type=CONTENT_TYPE)
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(
            "The fields name, parent must make a unique set.", response.data["message"][0]
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
