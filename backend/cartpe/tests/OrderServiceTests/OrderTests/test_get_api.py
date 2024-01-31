from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from auth_service.models import User
from shipping_service.models import Country, Address, UserAddress
from product_service.models import Product
from order_service.models import Order
from order_service.constants import OrderMethod
from payment_service.models import Payment

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
            line1 = "abc", line2 = "def", city = "pqr", state = "xyz", country = self.country, pin_code = "123244"
        )
        self.user_address = UserAddress.objects.create(
            name = "test_user", user = self.user, address = self.address, alternate_phone = "1234567890", type = "Home",
            is_default = False
        )
        self.product = Product.objects.create(name="Canon 80D", description="good product", price=50000, stock_count=10)
        self.order = Order.objects.create(
            user_address=self.user_address, amount=100, pending_amount=0, method=OrderMethod.COD, user=self.user
        )
        self.payment = Payment.objects.create(
            total_mrp = 2129.99, total_discount_price = 153, total_selling_price = 1976.99, convenience_fee = 10,
            shipping_fee = 0, total_amount = 1987, round_off_price = 0.01, savings_amount = 143, savings_percent = 6.71,
            order = self.order
        )

    def test_get_order_list_success(self):
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
            line1 = "abc", line2 = "def", city = "pqr", state = "xyz", country = self.country, pin_code = "123244"
        )
        self.user_address = UserAddress.objects.create(
            name = "test_user", user = self.user, address = self.address, alternate_phone = "1234567890", type = "Home",
            is_default = False
        )
        self.product = Product.objects.create(name="Canon 80D", description="good product", price=50000, stock_count=10)
        self.order = Order.objects.create(
            user_address=self.user_address, amount=100, pending_amount=0, method=OrderMethod.COD, user=self.user
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
