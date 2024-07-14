from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from product_service.models import Brand
from auth_service.models import User

CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()


class UpdateBrandByIdTest(APITestCase):
    """Test module for PATCH request for BrandByIdAPIView API"""

    def get_url(self, brand_id):
        url = reverse("brand_by_id", kwargs={"id": brand_id})
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        self.google = Brand.objects.create(name="Google", description="good brand")

    def test_update_with_valid_data(self):
        url = self.get_url(self.google.id)
        data = json.dumps({"id": 20, "name": "abc", "description": "amazing brand", "slug": "abcd"})
        response = client.patch(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.google.id, response.data["id"])
        self.assertEqual("abc", response.data["name"])
        self.assertEqual("amazing brand", response.data["description"])
        self.assertEqual("abc", response.data["slug"])

    def test_update_with_empty_input_field(self):
        url = self.get_url(self.google.id)
        data = json.dumps({"name": ""})
        response = client.patch(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual("This field may not be blank.", response.data["name"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_with_non_existing_id(self):
        url = self.get_url(1000)
        data = json.dumps({"name": "abc"})
        response = client.patch(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual("Unable to find brand with id 1000", response.data["message"])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_update_with_same_name(self):
        url = self.get_url(self.google.id)
        data = json.dumps({"name": "Google"})
        response = client.patch(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(
            "Brand 'Google' already exists and cannot be created or updated again.",
            response.data["message"][0],
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
