from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.exceptions import ValidationError
from unittest.mock import patch
import json
from cart_service.serializers import CartSerializer
from product_service.models import Product
from auth_service.models import User
import redis

# Initialize the APIClient app
client = APIClient()

# Global variables
CONTENT_TYPE = "application/json"

# Initialise JSON redis instance
redis_client = redis.Redis().json()

class PostCartItemsAPITest(APITestCase):
    """ Test module for POST request for CartAPIView API """

    def setUp(self):
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.product = Product.objects.create(name = "iphone 13", description = "ok product", price = 70000, stock_count = 1)

    def get_url(self):
        url = reverse("cart")
        return url

    def get_redis_key(self):
        return "cart:%s" % self.user.id

    def test_post_with_valid_data(self):
        url = self.get_url()
        data = json.dumps({ "product": { "id" : self.product.id}, "quantity": 2 })
        response = client.post(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual({ "cartItems": [{ "product": { "id": self.product.id }, "quantity": 2 }]}, response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post_with_invalid_data(self):
        url = self.get_url()
        data = json.dumps({ "quantity": 2 })
        response = client.post(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("This field is required.", str(response.data["product"][0]))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_duplicate_product_id(self):
        url = self.get_url()
        data = json.dumps({ "product": { "id" : self.product.id }, "quantity": 2 })

        redis_client.set(self.get_redis_key(), "$", { "cartItems": [] })
        redis_client.arrappend(self.get_redis_key(), "$.cartItems", { "product": {"id" : 100 }, "quantity": 2 })
        redis_client.arrappend(self.get_redis_key(), "$.cartItems", { "product": {"id" : self.product.id }, "quantity": 2 })

        response = client.post(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("Product already exists in cart.", str(response.data["message"][0]))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    @patch("cart_service.serializers.redis_client")
    def test_redis_connection_error(self, mock_redis_client):
        mock_redis_client.get.side_effect = redis.ConnectionError

        data = { "product": { "id": 2 }, "quantity": 3 }
        serializer = CartSerializer(data = data, context = {"redis_key": self.get_redis_key() })
        with self.assertRaises(ValidationError) as response:
            serializer.is_valid(raise_exception = True)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.exception.status_code)
        self.assertEqual("Redis server is down.", response.exception.detail["message"][0])

    @patch("cart_service.serializers.redis_client")
    def test_redis_timeout_error(self, mock_redis_client):
        mock_redis_client.get.side_effect = redis.TimeoutError

        data = { "product": { "id": 2 }, "quantity": 3 }
        serializer = CartSerializer(data = data, context = { "redis_key": self.get_redis_key() })
        with self.assertRaises(ValidationError) as response:
            serializer.is_valid(raise_exception = True)

        self.assertEqual("Redis server is slow or unable to respond.", response.exception.detail["message"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.exception.status_code)

    def tearDown(self):
        redis_key = self.get_redis_key()
        if redis_client.get(redis_key):
            redis_client.delete(redis_key)