from django.test import TestCase
from product_service.models import Attribute, AttributeValue

class AttributeValueModelTest(TestCase):
    def setUp(self):
        self.color = Attribute.objects.create(name = "Color")
        self.greenColor = AttributeValue.objects.create(value = "Green", attribute = self.color)

    def test_str_is_equal_to_title(self):
        self.assertEqual(self.greenColor.value, str(AttributeValue.objects.get(value = "Green")))
