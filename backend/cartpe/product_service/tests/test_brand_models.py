from django.test import TestCase
from ..models import Brand

class ProductModelTest(TestCase):
    def setUp(self) -> None:
        Brand.objects.create(name="Google", description="google")

    def test_str_is_equal_to_title(self):
        product = Brand.objects.get(name__iexact = "google")
        self.assertEqual(str(product), product.name)