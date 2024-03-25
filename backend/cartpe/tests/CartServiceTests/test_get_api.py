from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, ProductVariant
from auth_service.models import User
import redis

# Initialize the APIClient app
client = APIClient()

CONTENT_TYPE = "application/json"

# Initialise JSON redis instance
redis_client = redis.Redis().json()

class GetCartItemsAPITest(APITestCase):
    """ Test module for GET request for CartAPIView API """

    def setUp(self):
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.product = Product.objects.create(name = "iphone 13", description = "ok product")
        self.productVariant = ProductVariant.objects.create(
            product = self.product, 
            images=['example1.jpg', 'example2.jpg'],
            price=70000,
            stock_count = 10
        )

    def get_url(self):
        url = reverse("cart")
        return url

    def get_redis_key(self):
        return "cart:%s" % self.user.id

    def test_get_empty_cart(self):
        url = self.get_url()
        response = client.get(url)

        self.assertEqual({ "cartItems": [] }, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_all_cart_items(self):
        redis_client.set(self.get_redis_key(), "$", { "cartItems": [] })
        redis_client.arrappend(self.get_redis_key(), "$.cartItems", { "product": { "id": 1 }, "quantity": 2 })

        url = self.get_url()
        response = client.get(url)

        self.assertEqual({ "cartItems": [{ "product": { "id": 1 }, "quantity": 2 }]}, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def tearDown(self):
        redis_key = self.get_redis_key()
        if redis_client.get(redis_key):
            redis_client.delete(redis_key)