from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from shipping_service.models import Country, Address, UserAddress
from order_service.models import Order
from auth_service.models import User
from order_service.constants import OrderMethod, OrderStatus, OrderRefundStatus
from payment_service.models import Payment
from unittest.mock import patch
import json

CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()

class UpdateOrderByIdAPIView(APITestCase):
    """ Test module for PATCH request for OrderByIdAPIView API """

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
            method=OrderMethod.UPI, user_address=self.user_address, amount=123.00, amount_due=0.00,
            amount_paid=123.00, amount_refundable=0.00, user=self.user
        )
        self.payment = Payment.objects.create(
            total_mrp = 2129.99, total_discount_price = 153, total_selling_price = 1976.99, convenience_fee = 10,
            shipping_fee = 0, total_amount = 1987, round_off_price = 0.01, savings_amount = 143, savings_percent = 6.71,
            order = self.order
        )

    @patch("order_service.views.cache")
    def test_update_with_valid_data(self, mock_cache):
        mock_cache.has_key.return_value = None

        url = self.get_url(self.order.id)
        data = json.dumps({ "status": OrderStatus.CANCELLED })
        response = client.patch(url, data=data, content_type=CONTENT_TYPE)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(OrderStatus.CANCELLED, response.data["status"])
        self.assertEqual(Decimal(self.order.amount_paid), response.data["amount_refundable"])
        self.assertEqual(OrderRefundStatus.COMPLETED, response.data["refund_status"])
        mock_cache.delete.assert_not_called()

    @patch("order_service.views.cache")
    def test_update_with_delete_cached_data(self, mock_cache):
        mock_cache.has_key.return_value = True

        url = self.get_url(self.order.id)
        response = client.patch(
            url, data=json.dumps({ "status": OrderStatus.CANCELLED }), content_type=CONTENT_TYPE
        )

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(OrderStatus.CANCELLED, response.data["status"])
        self.assertEqual(Decimal(self.order.amount_paid), response.data["amount_refundable"])
        self.assertEqual(OrderRefundStatus.COMPLETED, response.data["refund_status"])
        mock_cache.delete.assert_called_once()

    @patch("order_service.views.cache")
    def test_get_with_invalid_data(self, mock_cache):
        mock_cache.has_key.return_value = None

        url = self.get_url(1000)
        response = client.patch(
            url, data=json.dumps({ "status": OrderStatus.CANCELLED }), content_type=CONTENT_TYPE
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual("Unable to find order with id 1000", response.data["message"])
        mock_cache.delete.assert_not_called()

    @patch("order_service.views.cache")
    def test_update_with_invalid_data(self, mock_cache):
        mock_cache.has_key.return_value = None

        url = self.get_url(self.order.id)
        response = client.patch(
            url, data=json.dumps({ "status": "Cancel" }), content_type=CONTENT_TYPE
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('"Cancel" is not a valid choice.', str(response.data["status"][0]))
        mock_cache.delete.assert_not_called()
