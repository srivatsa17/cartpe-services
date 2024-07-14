from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, ProductVariant, WishList
from auth_service.models import User
from unittest.mock import patch

# Initialize the APIClient app
client = APIClient()


class GetAllWishlistTest(APITestCase):
    """Test module for GET request for WishListAPIView API"""

    def get_url(self):
        url = reverse("wishlist")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        self.product = Product.objects.create(name="iphone 13", description="ok product")
        self.productVariant = ProductVariant.objects.create(
            product=self.product,
            images=["example1.jpg", "example2.jpg"],
            price=70000,
            stock_count=10,
        )
        self.wishlist = WishList.objects.create(product_variant=self.productVariant, user=self.user)

    @patch("product_service.views.cache")
    def test_get_with_valid_data(self, mock_cache):
        mock_cache.has_key.return_value = None

        url = self.get_url()
        response = client.get(url)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @patch("product_service.views.cache")
    def test_get_with_valid_cached_data(self, mock_cache):
        mock_cache.get.return_value = {
            "id": 123,
            "product": {
                "id": 134,
                "name": "abc",
                "slug": "abc",
                "description": "abcd",
                "brand": "xyz",
                "category": "pqr",
                "categorySlug": "pqr",
            },
            "productVariant": {
                "id": 162,
                "productId": 134,
                "name": "abc - red-L",
                "sku": "84b657ce-1074-4252-b16f-348a095e2c9e",
                "images": ["example.jpg"],
                "price": 499.99,
                "discount": 10,
                "discountedPrice": 50.0,
                "sellingPrice": 449.99,
                "stockCount": 150,
                "properties": [
                    {"id": 92, "propertyId": 2, "name": "size", "value": "L"},
                    {"id": 100, "propertyId": 1, "name": "color", "value": "red"},
                ],
                "availableProperties": ["size", "color"],
                "createdAt": "21 Feb 2024, 22:58",
                "updatedAt": "21 Feb 2024, 22:58",
            },
            "createdAt": "26 Feb 2024, 22:21",
            "updatedAt": "26 Feb 2024, 22:21",
        }

        url = self.get_url()
        with patch("product_service.views.cache.set") as mock_set:
            response = client.get(url)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        mock_set.assert_not_called()


class GetWishListByIdTest(APITestCase):
    """Test module for GET request for WishListByIdAPIView API"""

    def get_url(self, wishlist_id):
        url = reverse("wishlist_by_id", kwargs={"id": wishlist_id})
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        self.product = Product.objects.create(name="iphone 13", description="ok product")
        self.productVariant = ProductVariant.objects.create(
            product=self.product,
            images=["example1.jpg", "example2.jpg"],
            price=70000,
            stock_count=10,
        )
        self.wishlist = WishList.objects.create(product_variant=self.productVariant, user=self.user)

    def test_get_with_valid_id(self):
        url = self.get_url(self.wishlist.id)
        response = client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data)

    def test_get_with_non_existing_id(self):
        url = self.get_url(1000)
        response = client.get(url)

        self.assertEqual(
            "Unable to find wishlist product with id 1000", str(response.data["message"])
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
