from django.test import TestCase
from product_service.models import Product, ProductReview
from auth_service.models import User

class ProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        self.product = Product.objects.create(name="pixel 7", description="good product")
        self.product_review = ProductReview.objects.create(
            product=self.product, user=self.user, headline="Amazing product", rating=5
        )
    
    def test_str_is_equal_to_title(self):
        self.assertEqual(str(self.product_review.id), str(ProductReview.objects.get(id = self.product_review.id)))
