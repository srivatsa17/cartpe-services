from django.test import TestCase
from product_service.models import (
    Product,
    ProductVariant,
    ProductVariantProperty,
    ProductVariantPropertyValue,
)


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="pixel 7", description="good product")
        self.productVariant = ProductVariant.objects.create(
            product=self.product,
            images=["example1.jpg", "example2.jpg"],
            price=70000,
            stock_count=10,
        )
        self.property = ProductVariantProperty.objects.create(name="color")
        self.propertyValue = ProductVariantPropertyValue.objects.create(
            property=self.property, value="blue"
        )

    def test_str_is_equal_to_title(self):
        self.assertEqual(self.product.name, str(Product.objects.get(id=self.product.id)))
        self.assertEqual(
            self.productVariant.name, str(ProductVariant.objects.get(id=self.productVariant.id))
        )
        self.assertEqual(
            self.property.name, str(ProductVariantProperty.objects.get(id=self.property.id))
        )
        self.assertEqual(
            "%s" % self.propertyValue,
            str(ProductVariantPropertyValue.objects.get(id=self.property.id)),
        )
