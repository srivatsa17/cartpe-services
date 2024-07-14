from django.test import TestCase
from product_service.models import Product, Category
from product_service.filters import ProductFilter


class ProductFilterTestCase(TestCase):
    """Test module for filters applied on Product model"""

    def setUp(self):
        self.root_category = Category.objects.create(name="Root Category")
        self.child_category = Category.objects.create(
            name="Child Category", parent=self.root_category
        )

        self.filter_instance = ProductFilter()

    def test_filter_category_name(self):
        queryset = Product.objects.all()
        filtered_queryset = self.filter_instance.filter_category_name(
            queryset, "category", "Child Category"
        )

        expected_queryset = queryset.filter(
            category__in=self.child_category.get_descendants(include_self=True)
        )
        self.assertQuerysetEqual(filtered_queryset, expected_queryset)
