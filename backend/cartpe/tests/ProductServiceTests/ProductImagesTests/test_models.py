from django.test import TestCase
from product_service.models import Image, Product

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name = "Canon 80 D", description = "good product", price = 50000, stock_count = 10
        )
        self.sample_image = "https://cartpe.s3.ap-south-1.amazonaws.com/Products/Canon+80D/canon_80D_image_1.webp"
        self.image_instance = Image.objects.create(image = self.sample_image, is_featured = True, product = self.product)

    def test_str_is_equal_to_title(self):
        self.assertEqual(self.sample_image, str(Image.objects.get(id = self.image_instance.id)))
