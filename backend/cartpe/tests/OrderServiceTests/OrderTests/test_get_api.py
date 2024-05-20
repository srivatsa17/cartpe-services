from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from auth_service.models import User
from shipping_service.models import Country, Address, UserAddress
from order_service.models import Order
from order_service.constants import OrderMethod
from payment_service.models import Payment
from unittest.mock import patch

# Global variables
CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()

class OrderAPITestCase(APITestCase):
    """ Test module for GET request to OrderAPIView API """

    def get_url(self):
        url = reverse("orders")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)
        self.country = Country.objects.create(name = "India")
        self.address = Address.objects.create(
            building = "abc", area = "def", city = "pqr", state = "xyz", country = self.country, pin_code = "123244"
        )
        self.user_address = UserAddress.objects.create(
            name = "test_user", user = self.user, address = self.address, alternate_phone = "1234567890", type = "Home",
            is_default = False
        )
        self.order = Order.objects.create(
            method=OrderMethod.COD, user_address=self.user_address, amount=123.00, amount_due=123.00,
            amount_paid=0.00, amount_refundable=0.00, user=self.user
        )
        self.payment = Payment.objects.create(
            total_mrp = 2129.99, total_discount_price = 153, total_selling_price = 1976.99, convenience_fee = 10,
            shipping_fee = 0, total_amount = 1987, round_off_price = 0.01, savings_amount = 143, savings_percent = 6.71,
            order = self.order
        )

    @patch('order_service.views.cache')
    def test_get_order_list_success(self, mock_cache):
        url = self.get_url()
        mock_cache.get.return_value = {}

        with patch('order_service.views.cache.set') as mock_set:
            response = client.get(url)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        mock_set.assert_not_called()

    @patch('order_service.views.cache')
    def test_get_order_list_cached_success(self, mock_cache):
        mock_cache.has_key.return_value = None

        url = self.get_url()
        response = client.get(url)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

class OrderByIdAPITestCase(APITestCase):
    """ Test module for GET request to OrderByIdAPIView API """

    def get_url(self, order_id):
        url = reverse("order_by_id", kwargs = { "id" : order_id })
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)
        self.country = Country.objects.create(name = "India")
        self.address = Address.objects.create(
            building = "abc", area = "def", city = "pqr", state = "xyz", country = self.country, pin_code = "123244"
        )
        self.user_address = UserAddress.objects.create(
            name = "test_user", user = self.user, address = self.address, alternate_phone = "1234567890", type = "Home",
            is_default = False
        )
        self.order = Order.objects.create(
            method=OrderMethod.COD, user_address=self.user_address, amount=123.00, amount_due=123.00,
            amount_paid=0.00, amount_refundable=0.00, user=self.user
        )
        self.payment = Payment.objects.create(
            total_mrp = 2129.99, total_discount_price = 153, total_selling_price = 1976.99, convenience_fee = 10,
            shipping_fee = 0, total_amount = 1987, round_off_price = 0.01, savings_amount = 143, savings_percent = 6.71,
            order = self.order
        )

    def test_get_order_success(self):
        url = self.get_url(self.order.id)
        response = client.get(url)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_order_not_found(self):
        url = self.get_url(1000)
        response = client.get(url)

        self.assertEqual("Unable to find order with id 1000", str(response.data["message"]))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
