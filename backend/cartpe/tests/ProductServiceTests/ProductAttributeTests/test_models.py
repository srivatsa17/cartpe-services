from django.test import TestCase
from product_service.models import Attribute

class AttributeModelTest(TestCase):
    def setUp(self):
        self.color = Attribute.objects.create(name = "Color")

    def test_str_is_equal_to_title(self):
        self.assertEqual(self.color.name, str(Attribute.objects.get(name = "Color")))
