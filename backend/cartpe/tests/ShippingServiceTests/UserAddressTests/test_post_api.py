from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from shipping_service.models import Country
from auth_service.models import User

CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()


class PostUserAddressTest(APITestCase):
    """Test module for POST request for UserAddressAPIView API"""

    def get_url(self):
        url = reverse("user_address")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        self.country = Country.objects.create(name="India")
        self.valid_data = {
            "name": "abc",
            "alternate_phone": "1234567890",
            "type": "Home",
            "is_default": True,
            "address": {
                "building": "abc",
                "area": "def",
                "city": "pqr",
                "state": "xyz",
                "country": "India",
                "pin_code": "123244",
            },
        }

    def test_post_with_valid_data(self):
        url = self.get_url()
        data = json.dumps(self.valid_data)
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIsNotNone(response.data)

    def test_post_with_existing_default_address(self):
        url = self.get_url()
        data = json.dumps(self.valid_data)
        client.post(url, data=data, content_type=CONTENT_TYPE)
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        response1 = client.get(url)

        self.assertFalse(response1.data[0]["is_default"])
        self.assertTrue(response1.data[1]["is_default"])
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post_with_missing_fields(self):
        url = self.get_url()
        data = json.dumps({})
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual("This field is required.", response.data["name"][0])
        self.assertEqual("This field is required.", response.data["alternate_phone"][0])
        self.assertEqual("This field is required.", response.data["type"][0])
        self.assertEqual("This field is required.", response.data["is_default"][0])
        self.assertEqual("This field is required.", response.data["address"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
