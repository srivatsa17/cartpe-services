from django.test import TestCase
from product_service.models import Brand

class ProductModelTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name = "Google", description = "google")

    def test_str_is_equal_to_title(self):
        self.assertEqual(self.brand.name, str(Brand.objects.get(name__iexact = "google")))