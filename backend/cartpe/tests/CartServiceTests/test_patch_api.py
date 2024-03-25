from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.exceptions import ValidationError
from unittest.mock import patch
import json
from cart_service.serializers import CartByIdSerializer
from cart_service.views import CartByIdAPIView
from product_service.models import Product, ProductVariant
from auth_service.models import User
import redis

# Initialize the APIClient app
client = APIClient()

# Global variables
CONTENT_TYPE = "application/json"

# Initialise JSON redis instance
redis_client = redis.Redis().json()

class UpdateCartItemsAPITest(APITestCase):
    """ Test module for PATCH request for CartByIdAPIView API """

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

    def get_url(self, product_id):
        url = reverse("cart_by_id", kwargs = { "id" : product_id })
        return url

    def get_redis_key(self):
        return "cart:%s" % self.user.id

    def test_update_with_valid_data(self):
        redis_client.set(self.get_redis_key(), "$", { "cartItems": [] })
        redis_client.arrappend(self.get_redis_key(), "$.cartItems", { "product": {"id" : self.product.id }, "quantity": 2 })

        url = self.get_url(self.product.id)
        data = json.dumps({ "quantity": 5 })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual({ "cartItems": [{ "product": { "id": self.product.id }, "quantity": 5 }]}, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_update_empty_cart(self):
        url = self.get_url(self.product.id)
        data = json.dumps({ "quantity": 5 })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("Empty cart found for user.", str(response.data["message"][0]))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    @patch("cart_service.serializers.redis_client")
    def test_update_with_invalid_path(self, mock_redis_client):
        def mock_get_side_effect(key, path=None):
            return None if path == "$.cartItems" else ""

        mock_redis_client.get.side_effect = mock_get_side_effect

        data = { "quantity": 3 }
        serializer = CartByIdSerializer(data = data, context = { "redis_key": self.get_redis_key() })
        with self.assertRaises(ValidationError) as response:
            serializer.is_valid(raise_exception = True)

        self.assertEqual("CartItems not found.", response.exception.detail["message"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.exception.status_code)

    def test_update_with_unknown_cart_item(self):
        url = self.get_url(1000)

        redis_client.set(self.get_redis_key(), "$", { "cartItems": [] })
        redis_client.arrappend(self.get_redis_key(), "$.cartItems", { "product": { "id" : self.product.id }, "quantity": 2 })

        data = json.dumps({ "quantity": 5 })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("Requested cart item is not found.", str(response.data["message"][0]))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_with_same_quantity(self):
        url = self.get_url(self.product.id)

        redis_client.set(self.get_redis_key(), "$", { "cartItems": [] })
        redis_client.arrappend(self.get_redis_key(), "$.cartItems", { "product": { "id" : self.product.id }, "quantity": 5 })

        data = json.dumps({ "quantity": 5 })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("New quantity provided is same as previous quantity.", str(response.data["message"][0]))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    @patch("cart_service.views.redis_client")
    def test_update_on_empty_cart(self, mock_redis_client):
        mock_redis_client.get.return_value = None

        response = CartByIdAPIView.get_cart_list(self, redis_key = self.get_redis_key())

        self.assertEqual({ "cartItems": [] }, response)

    @patch("cart_service.serializers.redis_client")
    def test_redis_connection_error(self, mock_redis_client):
        mock_redis_client.get.side_effect = redis.ConnectionError

        data = { "quantity": 3 }
        serializer = CartByIdSerializer(data = data, context = { "redis_key": self.get_redis_key() })
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception = True)

        self.assertEqual("Redis server is down.", context.exception.detail["message"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, context.exception.status_code)

    @patch("cart_service.serializers.redis_client")
    def test_redis_timeout_error(self, mock_redis_client):
        mock_redis_client.get.side_effect = redis.TimeoutError

        data = { "quantity": 3 }
        serializer = CartByIdSerializer(data = data, context = { "redis_key": self.get_redis_key() })
        with self.assertRaises(ValidationError) as response:
            serializer.is_valid(raise_exception = True)

        self.assertEqual("Redis server is slow or unable to respond.", response.exception.detail["message"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.exception.status_code)

    def tearDown(self):
        redis_key = self.get_redis_key()
        if redis_client.get(redis_key):
            redis_client.delete(redis_key)