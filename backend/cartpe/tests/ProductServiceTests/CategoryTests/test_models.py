from django.test import TestCase
from product_service.models import Category
from django.utils.text import slugify


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Men", description="Clothing", parent=None)
        self.child_category = Category.objects.create(name="Men Topwear", parent=self.category)

    def test_str_is_equal_to_title(self):
        self.assertEqual(self.category.name, str(Category.objects.get(name="Men")))

    def test_slug_without_parent_duplication(self):
        # Check if the slug is correctly generated without parent duplication
        category = Category.objects.get(name="Men Topwear")
        self.assertEqual(category.slug, slugify("Men Topwear"))
