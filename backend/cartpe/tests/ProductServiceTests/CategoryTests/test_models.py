from django.test import TestCase
from product_service.models import Category


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Men", description="Clothing", parent=None)

    def test_str_is_equal_to_title(self):
        self.assertEqual(self.category.name, str(Category.objects.get(name="Men")))
