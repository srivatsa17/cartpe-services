from django.test import TestCase
from product_service.models import Brand

class ProductModelTest(TestCase):
    def setUp(self) -> None:
        Brand.objects.create(name = "Google", description = "google")

    def test_str_is_equal_to_title(self):
        brand = Brand.objects.get(name__iexact = "google")
        expectedResponse = brand.name
        receivedResponse = str(brand)

        self.assertEqual(receivedResponse, expectedResponse)