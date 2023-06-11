from django.test import TestCase
from product_service.models import Product

class ProductModelTest(TestCase):
    def setUp(self) -> None:
        self.product = Product.objects.create(name="pixel 7", description="good product", price=50000, stock_count=10)

    def test_str_is_equal_to_title(self):
        expectedResponse = self.product.name
        receivedResponse = str(self.product)

        self.assertEqual(receivedResponse, expectedResponse)
