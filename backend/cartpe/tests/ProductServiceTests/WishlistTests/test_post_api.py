from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, ProductVariant, WishList
from auth_service.models import User
from unittest.mock import patch
import json

CONTENT_TYPE = "application/json"
SAMPLE_IMAGE = (
    "https://cartpe.s3.ap-south-1.amazonaws.com/Products/Canon+80D/canon_80D_image_1.webp"
)

# Initialize the APIClient app
client = APIClient()


class PostWishlistTest(APITestCase):
    """Test module for POST request for WishListAPIView API"""

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

    @patch("product_service.views.cache")
    def test_post_with_valid_data(self, mock_cache):
        mock_cache.has_key.return_value = None

        url = self.get_url()
        response = client.post(
            url,
            data=json.dumps({"product_variant": self.productVariant.id}),
            content_type=CONTENT_TYPE,
        )

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    @patch("product_service.views.cache")
    def test_post_with_delete_cached_data(self, mock_cache):
        mock_cache.has_key.return_value = True

        url = self.get_url()
        response = client.post(
            url,
            data=json.dumps({"product_variant": self.productVariant.id}),
            content_type=CONTENT_TYPE,
        )

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        mock_cache.delete.assert_called_once()

    @patch("product_service.views.cache")
    def test_post_with_existing_wishlist_data(self, mock_cache):
        mock_cache.has_key.return_value = None

        url = self.get_url()
        WishList.objects.create(product_variant=self.productVariant, user=self.user)

        response = client.post(
            url,
            data=json.dumps({"product_variant": self.productVariant.id}),
            content_type=CONTENT_TYPE,
        )

        self.assertEqual("Product is already in wishlist.", str(response.data["message"][0]))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    @patch("product_service.views.cache")
    def test_get_with_invalid_data(self, mock_cache):
        mock_cache.has_key.return_value = None

        url = self.get_url()
        response = client.post(
            url, data=json.dumps({"product_variant": 1000}), content_type=CONTENT_TYPE
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
