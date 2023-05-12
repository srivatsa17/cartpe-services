from django.test import TestCase
from product_service.models import Attribute

class ProductModelTest(TestCase):
    def setUp(self) -> None:
        self.color = Attribute.objects.create(name="Color")

    def test_str_is_equal_to_title(self):
        attribute = Attribute.objects.get(name = "Color")
        expectedResponse = self.color.name
        receivedResponse = str(attribute)

        self.assertEqual(receivedResponse, expectedResponse)