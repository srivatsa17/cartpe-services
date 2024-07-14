from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, ProductVariant
from auth_service.models import User
from django.core.cache import cache

# Initialize the APIClient app
client = APIClient()


class GetCartItemsAPITest(APITestCase):
    """Test module for GET request for CartAPIView API"""

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

    def test_get_empty_cart(self):
        url = self.get_url()
        response = client.get(url)

        self.assertEqual({"cartItems": []}, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_all_cart_items(self):
        cache_data = {"cartItems": [{"product": {"id": self.product.id}, "quantity": 2}]}
        cache.set(self.get_redis_key(), cache_data, timeout=2)

        url = self.get_url()
        response = client.get(url)

        self.assertEqual(
            {"cartItems": [{"product": {"id": self.product.id}, "quantity": 2}]}, response.data
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def tearDown(self):
        cache.delete(self.get_redis_key())
