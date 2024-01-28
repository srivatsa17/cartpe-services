from django.test import TestCase
from auth_service.models import User
from product_service.models import Product
from shipping_service.models import Country, Address, UserAddress
from order_service.models import Order
from payment_service.models import Payment

class PaymentModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name = "India")
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        self.address = Address.objects.create(
            line1 = "abc", line2 = "def", city = "pqr", state = "xyz", country = self.country, pin_code = "123244"
        )
        self.user_address = UserAddress.objects.create(
            name = "test_user", user = self.user, address = self.address, alternate_phone = "1234567890", type = "Home",
            is_default = False
        )
        self.product = Product.objects.create(name="Canon 80D", description="good product", price=50000, stock_count=10)
        self.order = Order.objects.create(
            method="Cash On Delivery", user_address=self.user_address, amount=123.00, pending_amount=0, user=self.user
        )
        self.payment = Payment.objects.create(
            total_mrp = 2129.99, total_discount_price = 153, total_selling_price = 1976.99, convenience_fee = 10,
            shipping_fee = 0, total_amount = 1987, round_off_price = 0.01, savings_amount = 143, savings_percent = 6.71,
            order = self.order
        )

    def test_str_is_equal_to_title(self):
        self.assertEqual(str(self.payment.pk), str(Payment.objects.get(id = self.payment.id)))
