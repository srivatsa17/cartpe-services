from django.test import TestCase
from product_service.models import Product, ProductVariant, WishList
from auth_service.models import User

class WishlistModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        self.product = Product.objects.create(name="pixel 7", description="good product")
        self.productVariant = ProductVariant.objects.create(
            product = self.product, 
            images=['example1.jpg', 'example2.jpg'],
            price=70000,
            stock_count = 10
        )
        self.wishlist = WishList.objects.create(product_variant = self.productVariant, user = self.user)

    def test_str_is_equal_to_title(self):
        self.assertEqual(str(self.wishlist.pk), str(WishList.objects.get(id = self.wishlist.id)))

