from django.test import TestCase
from auth_service.models import User
from product_service.models import Product, ProductVariant
from shipping_service.models import Country, Address, UserAddress
from order_service.models import Order, OrderItem
from order_service.constants import OrderMethod


class OrderItemModelTest(TestCase):
    def setUp(self) -> None:
        self.country = Country.objects.create(name="India")
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        self.address = Address.objects.create(
            building="abc",
            area="def",
            city="pqr",
            state="xyz",
            country=self.country,
            pin_code="123244",
        )
        self.user_address = UserAddress.objects.create(
            name="test_user",
            user=self.user,
            address=self.address,
            alternate_phone="1234567890",
            type="Home",
            is_default=False,
        )
        self.product = Product.objects.create(name="iphone 13", description="ok product")
        self.productVariant = ProductVariant.objects.create(
            product=self.product,
            images=["example1.jpg", "example2.jpg"],
            price=70000,
            stock_count=10,
        )
        self.order = Order.objects.create(
            method=OrderMethod.COD,
            user_address=self.user_address,
            amount=123.00,
            amount_due=123.00,
            amount_paid=0.00,
            amount_refundable=0.00,
            user=self.user,
        )
        self.orderItem = OrderItem.objects.create(
            order=self.order, product_variant=self.productVariant, quantity=2
        )

    def test_str_is_equal_to_title(self):
        self.assertEqual(str(self.orderItem.pk), str(OrderItem.objects.get(id=self.orderItem.id)))
