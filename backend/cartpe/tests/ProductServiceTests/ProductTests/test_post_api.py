from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from product_service.models import Category, Brand
from auth_service.models import User

CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()

class PostProductTest(APITestCase):
    """ Test module for POST request for ProductAPIView API """

    def get_url(self):
        url = reverse("products")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.category = Category.objects.create(name = "Electronics")
        self.brand = Brand.objects.create(name = "Cannon")
        self.valid_data = {
            "name" : "DSLR",
            "description" : "Amazing",
            "brand" : "Cannon",
            "category" : "Electronics",
            "price" : 929.99,
            "stock_count" : 5,
            "discount" : 0
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

        self.assertEqual("This field is required.", response.data["name"][0])
        self.assertEqual("This field is required.", response.data["description"][0])
        self.assertEqual("This field is required.", response.data["price"][0])
        self.assertEqual("This field is required.", response.data["brand"][0])
        self.assertEqual("This field is required.", response.data["stock_count"][0])
        self.assertEqual("This field is required.", response.data["discount"][0])
        self.assertEqual("This field is required.", response.data["category"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_with_same_name(self):
        url = self.get_url()
        data = json.dumps(self.valid_data)
        client.post(url, data = data, content_type = CONTENT_TYPE)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("Product 'DSLR' already exists and cannot be created or updated again.", response.data["message"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)