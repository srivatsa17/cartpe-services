from django.test import TestCase
from product_service.models import Product, Category, AttributeValue
from product_service.filters import ProductFilter

class ProductFilterTestCase(TestCase):
    """ Test module for filters applied on Product model """
    def setUp(self):
        self.root_category = Category.objects.create(name='Root Category')
        self.child_category = Category.objects.create(name='Child Category', parent=self.root_category)
        self.attribute_value = AttributeValue.objects.create(value='Test Value')

        self.filter_instance = ProductFilter()

    def test_filter_category_name(self):
        queryset = Product.objects.all()
        filtered_queryset = self.filter_instance.filter_category_name(queryset, 'category', 'Child Category')

        expected_queryset = queryset.filter(category__in=self.child_category.get_descendants(include_self=True))
        self.assertQuerysetEqual(filtered_queryset, expected_queryset)
    
    def test_filter_attribute_value(self):
        queryset = Product.objects.all()
        filtered_queryset = self.filter_instance.filter_attribute_value(queryset, 'attributes', 'Test Value')

        expected_queryset = queryset.filter(attributes__attribute_values=self.attribute_value)
        self.assertQuerysetEqual(filtered_queryset, expected_queryset)
