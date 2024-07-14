from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from product_service.models import Product, ProductVariant
from auth_service.models import User
from django.core.cache import cache

# Initialize the APIClient app
client = APIClient()

# Global variables
CONTENT_TYPE = "application/json"


class PostCartItemsAPITest(APITestCase):
    """Test module for POST request for CartAPIView API"""

    def setUp(self):
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        self.product = Product.objects.create(name="iphone 13", description="ok product")
        self.productVariant = ProductVariant.objects.create(
            product=self.product,
            images=["example1.jpg", "example2.jpg"],
            price=70000,
            stock_count=10,
        )

    def get_url(self):
        url = reverse("cart")
        return url

    def get_redis_key(self):
        return "user:{user}:cart".format(user=self.user)

    def test_post_with_valid_data(self):
        url = self.get_url()
        data = json.dumps({"product": {"id": 20}, "quantity": 2})
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual({"cartItems": [{"product": {"id": 20}, "quantity": 2}]}, response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post_with_invalid_data(self):
        url = self.get_url()
        data = json.dumps({"quantity": 2})
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual("This field is required.", str(response.data["product"][0]))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_with_duplicate_product_id(self):
        url = self.get_url()
        data = json.dumps({"product": {"id": self.product.id}, "quantity": 2})

        cache.set(
            self.get_redis_key(),
            {"cartItems": [{"product": {"id": self.product.id}, "quantity": 2}]},
            timeout=2,
        )

        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual("Product already exists in cart.", str(response.data["message"][0]))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def tearDown(self):
        cache.delete(self.get_redis_key())
