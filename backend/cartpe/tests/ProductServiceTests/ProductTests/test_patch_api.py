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
    """ Test module for PATCH request for ProductByIdAPIView API """

    def get_url(self, product_id):
        url = reverse("product_by_id", kwargs = { "id" : product_id })
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.category = Category.objects.create(name = "Electronics")
        self.pixel = Product.objects.create(name="pixel 7", description="good product", price=50000, stock_count=10, discount=0)

    def test_update_fields(self):
        Brand.objects.create(name = "apple")
        Category.objects.create(name = "Phone")

        url = self.get_url(self.pixel.id)
        data = json.dumps({
            "id" : 20,
            "name": "abc",
            "sku" : "a42c3fa7-a0be-45a9-ae06-61835f2cf64e",
            "description" : "good phone",
            "slug" : "abcd",
            "price" : 70000.90,
            "brand" : "apple",
            "stock_count" : 15,
            "discount" : 10,
            "category" : "Phone"
        })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual(self.pixel.id, response.data["id"])
        self.assertEqual("abc", response.data["name"])
        self.assertEqual(str(self.pixel.sku), response.data["sku"])
        self.assertEqual("good phone", response.data["description"]),
        self.assertEqual("abc", response.data["slug"])
        self.assertEqual(decimal.Decimal("70000.90"), response.data["price"])
        self.assertEqual("apple", response.data["brand"])
        self.assertEqual(15, response.data["stock_count"])
        self.assertEqual(10, response.data["discount"])
        self.assertEqual(decimal.Decimal("7000.09"), response.data["discounted_price"])
        self.assertEqual(decimal.Decimal("63000.81"), response.data["selling_price"])
        self.assertEqual("Phone", response.data["category"])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_update_with_empty_input_field(self):
        url = self.get_url(self.pixel.id)
        data = json.dumps({ "name" : "" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("This field may not be blank.", response.data["name"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_with_non_existing_id(self):
        url = self.get_url(1000)
        data = json.dumps({ "name" : "" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("Unable to find product with id 1000", response.data["message"])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_update_with_same_name(self):
        url = self.get_url(self.pixel.id)
        data = json.dumps({ "name" : "pixel 7" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("Product 'pixel 7' already exists and cannot be created or updated again.", response.data["message"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
