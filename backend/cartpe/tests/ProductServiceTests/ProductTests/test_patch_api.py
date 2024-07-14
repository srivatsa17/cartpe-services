from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json, decimal
from product_service.models import Product, Category, Brand
from auth_service.models import User

CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()


class UpdateProductByIdTest(APITestCase):
    """Test module for PATCH request for ProductByIdAPIView API"""

    def get_url(self, product_id):
        url = reverse("product_by_id", kwargs={"id": product_id})
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Electronics")
        self.pixel = Product.objects.create(name="pixel 7", description="good product")

    def test_update_fields(self):
        Brand.objects.create(name="apple")
        Category.objects.create(name="Phone")

        url = self.get_url(self.pixel.id)
        data = json.dumps(
            {
                "id": 20,
                "name": "abc",
                "description": "good phone",
                "slug": "abcd",
                "brand": "apple",
                "category": "Phone",
            }
        )
        response = client.patch(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(self.pixel.id, response.data["id"])
        self.assertEqual("abc", response.data["name"])
        self.assertEqual("good phone", response.data["description"]),
        self.assertEqual("abc", response.data["slug"])
        self.assertEqual("apple", response.data["brand"])
        self.assertEqual("Phone", response.data["category"])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_update_with_empty_input_field(self):
        url = self.get_url(self.pixel.id)
        data = json.dumps({"name": ""})
        response = client.patch(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual("This field may not be blank.", response.data["name"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_with_non_existing_id(self):
        url = self.get_url(1000)
        data = json.dumps({"name": ""})
        response = client.patch(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual("Unable to find product with id 1000", response.data["message"])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_update_with_same_name(self):
        url = self.get_url(self.pixel.id)
        data = json.dumps({"name": "pixel 7"})
        response = client.patch(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(
            "Product 'pixel 7' already exists and cannot be created again.",
            str(response.data["message"][0]),
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
