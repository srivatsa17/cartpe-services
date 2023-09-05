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

    def test_with_valid_data(self):
        expectedResponse = {"cartItems": [{"product": {"id": self.product.id}, "quantity": 2}]}
        expectedStatusCode = status.HTTP_201_CREATED

        url = self.get_url()
        data = json.dumps({ "product": {"id" : self.product.id}, "quantity": 2 })
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = response.data

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_invalid_data(self):
        expectedResponse = "This field is required."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({ "quantity": 2 })
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = str(response.data['product'][0])

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_duplicate_product_id(self):
        expectedResponse = "Product already exists in cart."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({ "product": {"id" : self.product.id}, "quantity": 2 })

        redis_client.set(self.get_redis_key(), '$', { "cartItems": [] })
        redis_client.arrappend(self.get_redis_key(), '$.cartItems', { "product": {"id" : 100 }, "quantity": 2 })
        redis_client.arrappend(self.get_redis_key(), '$.cartItems', { "product": {"id" : self.product.id }, "quantity": 2 })

        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = str(response.data["message"][0])

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    @patch('cart_service.serializers.redis_client')
    def test_redis_connection_error(self, mock_redis_client):
        mock_redis_client.get.side_effect = redis.ConnectionError
        expectedStatusCode = status.HTTP_400_BAD_REQUEST
        expectedResponse = "Redis server is down."

        data = {
            'product': { 'id': 2 },
            'quantity': 3
        }
        serializer = CartSerializer(data=data, context={'redis_key': self.get_redis_key() })
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        receivedResponse = context.exception.detail['message'][0]
        receivedStatusCode = context.exception.status_code
        self.assertEqual(expectedResponse, receivedResponse)
        self.assertEqual(expectedStatusCode, receivedStatusCode)

    @patch('cart_service.serializers.redis_client')
    def test_redis_timeout_error(self, mock_redis_client):
        mock_redis_client.get.side_effect = redis.TimeoutError
        expectedStatusCode = status.HTTP_400_BAD_REQUEST
        expectedResponse = "Redis server is slow or unable to respond."

        data = {
            'product': { 'id': 2 },
            'quantity': 3
        }
        serializer = CartSerializer(data = data, context = {'redis_key': self.get_redis_key() })
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception = True)

        receivedResponse = context.exception.detail['message'][0]
        receivedStatusCode = context.exception.status_code
        self.assertEqual(expectedResponse, receivedResponse)
        self.assertEqual(expectedStatusCode, receivedStatusCode)

    def tearDown(self) -> None:
        redis_key = self.get_redis_key()
        if redis_client.get(redis_key):
            redis_client.delete(redis_key)