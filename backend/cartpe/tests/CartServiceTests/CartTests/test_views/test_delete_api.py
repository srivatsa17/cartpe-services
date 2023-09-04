from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product
from auth_service.models import User
import redis

# Initialize the APIClient app
client = APIClient()

CONTENT_TYPE = "application/json"

# Initialise JSON redis instance
redis_client = redis.Redis().json()

class DeleteCartItemsAPITest(APITestCase):
    """ Test module for DELETE request for CartAPIView API """

    def setUp(self):
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.product = Product.objects.create(name = "iphone 13", description = "ok product", price = 70000, stock_count = 1)

    def get_url(self):
        url = reverse("cart")
        return url

    def test_with_valid_data(self):
        expectedResponse = None
        expectedStatusCode = status.HTTP_204_NO_CONTENT

        url = self.get_url()
        response = client.delete(url)
        receivedStatusCode = response.status_code
        receivedResponse = response.data

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

class DeleteCartItemsByIdAPITest(APITestCase):
    """ Test module for DELETE request for CartByIdAPIView API """

    def setUp(self):
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.product = Product.objects.create(name = "iphone 13", description = "ok product", price = 70000, stock_count = 1)

    def get_redis_key(self):
        return "cart:%s" % self.user.id

    def get_url(self, product_id):
        url = reverse('cart_by_id', kwargs = {'id' : product_id})
        return url

    def test_successful_delete(self):
        expectedResponse = { "cartItems": [] }
        expectedStatusCode = status.HTTP_200_OK

        redis_client.set(self.get_redis_key(), '$', { "cartItems": [] })
        redis_client.arrappend(self.get_redis_key(), '$.cartItems', { "product": {"id" : self.product.id }, "quantity": 2 })

        url = self.get_url(self.product.id)
        response = client.delete(url)
        receivedStatusCode = response.status_code
        receivedResponse = response.data

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_failure_delete(self):
        expectedResponse = "Empty cart found for user."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url(self.product.id)
        response = client.delete(url)
        receivedStatusCode = response.status_code
        receivedResponse = str(response.data["message"][0])

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def tearDown(self) -> None:
        redis_key = self.get_redis_key()
        if redis_client.get(redis_key):
            redis_client.delete(redis_key)