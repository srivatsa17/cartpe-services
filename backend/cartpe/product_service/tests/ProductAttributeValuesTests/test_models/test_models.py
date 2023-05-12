from django.test import TestCase
from product_service.models import Attribute, AttributeValue

class ProductModelTest(TestCase):
    def setUp(self) -> None:
        self.color = Attribute.objects.create(name="Color")
        self.greenColor = AttributeValue.objects.create(value="Green", attribute=self.color)

    def test_str_is_equal_to_title(self):
        attributeValue = AttributeValue.objects.get(value = "Green")
        expectedResponse = self.greenColor.value
        receivedResponse = str(attributeValue)

        self.assertEqual(receivedResponse, expectedResponse)