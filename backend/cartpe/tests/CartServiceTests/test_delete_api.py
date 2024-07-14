from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, ProductVariant
from auth_service.models import User
from django.core.cache import cache

# Initialize the APIClient app
client = APIClient()


class DeleteCartItemsAPITest(APITestCase):
    """Test module for DELETE request for CartAPIView API"""

    def setUp(self):
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        self.product = Product.objects.create(name="iphone 13", description="ok product")
        self.productVariant = ProductVariant.objects.create(
            product=self.product,
            images=["example1.jpg", "example2.jpg"],
            price=70000,
            stock_count=10,
        )

    def get_url(self):
        url = reverse("cart")
        return url

    def test_delete_with_valid_data(self):
        url = self.get_url()
        response = client.delete(url)

        self.assertIsNone(response.data)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)


class DeleteCartItemsByIdAPITest(APITestCase):
    """Test module for DELETE request for CartByIdAPIView API"""

    def setUp(self):
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        self.product = Product.objects.create(name="iphone 13", description="ok product")
        self.productVariant = ProductVariant.objects.create(
            product=self.product,
            images=["example1.jpg", "example2.jpg"],
            price=70000,
            stock_count=10,
        )

    def get_redis_key(self):
        return "user:{user}:cart".format(user=self.user)

    def get_url(self, product_id):
        url = reverse("cart_by_id", kwargs={"id": product_id})
        return url

    def test_delete_success(self):
        cache_data = {"cartItems": [{"product": {"id": self.product.id}, "quantity": 2}]}
        cache.set(self.get_redis_key(), cache_data, timeout=1)

        url = self.get_url(self.product.id)
        response = client.delete(url)

        self.assertEqual({"cartItems": []}, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete_with_empty_cart(self):
        cache_data = {"cartItems": []}
        cache.set(self.get_redis_key(), cache_data, timeout=2)

        url = self.get_url(self.product.id)
        response = client.delete(url)

        self.assertEqual("Cart is empty", str(response.data["message"][0]))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_delete_with_non_existing_product(self):
        cache_data = {"cartItems": [{"product": {"id": self.product.id}, "quantity": 2}]}
        cache.set(self.get_redis_key(), cache_data, timeout=2)

        url = self.get_url(self.product.id + 1)
        response = client.delete(url)

        self.assertEqual(
            f"Product with id = {self.product.id + 1} does not exist in the cart.",
            str(response.data["message"][0]),
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def tearDown(self):
        cache.delete(self.get_redis_key())
