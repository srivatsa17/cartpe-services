from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.exceptions import ValidationError
from unittest.mock import patch
import json
from cart_service.serializers import CartByIdSerializer
from cart_service.views import CartByIdAPIView
from product_service.models import Product
from auth_service.models import User
import redis

# Initialize the APIClient app
client = APIClient()

CONTENT_TYPE = "application/json"

# Initialise JSON redis instance
redis_client = redis.Redis().json()

class UpdateCartItemsAPITest(APITestCase):
    """ Test module for PATCH request for CartByIdAPIView API """

    def setUp(self):
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.product = Product.objects.create(name = "iphone 13", description = "ok product", price = 70000, stock_count = 1)

    def get_url(self, product_id):
        url = reverse('cart_by_id', kwargs = {'id' : product_id})
        return url

    def get_redis_key(self):
        return "cart:%s" % self.user.id

    def test_with_valid_data(self):
        expectedResponse = {"cartItems": [{"product": {"id": self.product.id}, "quantity": 5}]}
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.product.id)

        redis_client.set(self.get_redis_key(), '$', { "cartItems": [] })
        redis_client.arrappend(self.get_redis_key(), '$.cartItems', { "product": {"id" : self.product.id }, "quantity": 2 })

        data = json.dumps({ "quantity": 5 })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = response.data

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_empty_cart_update(self):
        expectedResponse = "Empty cart found for user."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url(self.product.id)
        data = json.dumps({ "quantity": 5 })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = str(response.data["message"][0])

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    @patch('cart_service.serializers.redis_client')
    def test_invalid_path_update(self, mock_redis_client):
        expectedStatusCode = status.HTTP_400_BAD_REQUEST
        expectedResponse = "CartItems not found."

        def mock_get_side_effect(key, path=None):
            if path == '$.cartItems':
                return None
            else:
                return ""

        mock_redis_client.get.side_effect = mock_get_side_effect

        data = { 'quantity': 3 }
        serializer = CartByIdSerializer(data = data, context = {'redis_key': self.get_redis_key() })
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception = True)

        receivedResponse = context.exception.detail['message'][0]
        receivedStatusCode = context.exception.status_code

        self.assertEqual(expectedResponse, receivedResponse)
        self.assertEqual(expectedStatusCode, receivedStatusCode)

    def test_unknown_cartItem_update(self):
        expectedResponse = "Requested cart item is not found."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url(1000)

        redis_client.set(self.get_redis_key(), '$', { "cartItems": [] })
        redis_client.arrappend(self.get_redis_key(), '$.cartItems', { "product": {"id" : self.product.id }, "quantity": 2 })

        data = json.dumps({ "quantity": 5 })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = str(response.data["message"][0])

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_same_quantity(self):
        expectedResponse = "New quantity provided is same as previous quantity."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url(self.product.id)

        redis_client.set(self.get_redis_key(), '$', { "cartItems": [] })
        redis_client.arrappend(self.get_redis_key(), '$.cartItems', { "product": {"id" : self.product.id }, "quantity": 5 })

        data = json.dumps({ "quantity": 5 })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = str(response.data["message"][0])

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    @patch('cart_service.views.redis_client')
    def test_empty_cart_response(self, mock_redis_client):
        mock_redis_client.get.return_value = None
        expectedResponse = {"cartItems": []}

        response = CartByIdAPIView.get_cart_list(self, redis_key = self.get_redis_key())

        self.assertEqual(response, expectedResponse)

    @patch('cart_service.serializers.redis_client')
    def test_redis_connection_error(self, mock_redis_client):
        mock_redis_client.get.side_effect = redis.ConnectionError
        expectedStatusCode = status.HTTP_400_BAD_REQUEST
        expectedResponse = "Redis server is down."

        data = {'quantity': 3}
        serializer = CartByIdSerializer(data=data, context={'redis_key': self.get_redis_key() })
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

        data = {'quantity': 3}
        serializer = CartByIdSerializer(data = data, context = {'redis_key': self.get_redis_key() })
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