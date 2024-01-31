from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from shipping_service.models import Country
from auth_service.models import User

CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()

class PostAddressTest(APITestCase):
    """ Test module for POST request for AddressAPIView API """

    def get_url(self):
        url = reverse("address")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.country = Country.objects.create(name = "India")
        self.valid_data = {
            "line1" : "abc",
            "line2" : "def",
            "city" : "pqr",
            "state" : "xyz",
            "country" : "India",
            "pin_code" : "123244"
        }

    def test_post_with_valid_data(self):
        url = self.get_url()
        data = json.dumps(self.valid_data)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post_with_missing_fields(self):
        url = self.get_url()
        data = json.dumps({})
        response = client.post(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("This field is required.", response.data["line1"][0])
        self.assertEqual("This field is required.", response.data["line2"][0])
        self.assertEqual("This field is required.", response.data["city"][0])
        self.assertEqual("This field is required.", response.data["state"][0])
        self.assertEqual("This field is required.", response.data["country"][0])
        self.assertEqual("This field is required.", response.data["pin_code"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
