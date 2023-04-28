from django.test import TestCase
from ..models import Product

class ProductModelTest(TestCase):
    def setUp(self) -> None:
        Product.objects.create(name="pixel 7", description="good product", brand="google", price=50000, stock_count=10)
    
    def test_str_is_equal_to_title(self):
        product = Product.objects.get(name = "pixel 7")
        self.assertEqual(str(product), product.name)
