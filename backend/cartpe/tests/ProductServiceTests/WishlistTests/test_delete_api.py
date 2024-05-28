from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, ProductVariant, WishList
from auth_service.models import User
from unittest.mock import patch

# Initialize the APIClient app
client = APIClient()

class DeleteWishlistByIdTest(APITestCase):
    """ Test module for DELETE request for WishListByIdAPIView API """

    def get_url(self, product_id):
        url = reverse("wishlist_by_id", kwargs = { "id": product_id })
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.product1 = Product.objects.create(name = "iphone 13", description = "ok product")
        self.productVariant = ProductVariant.objects.create(
            product = self.product1, 
            images=['example1.jpg', 'example2.jpg'],
            price=70000,
            stock_count = 10
        )
        self.wishlist = WishList.objects.create(product_variant = self.productVariant, user = self.user)

    def test_delete_with_existing_id(self):
        url = self.get_url(self.wishlist.id)
        response = client.delete(url)

        self.assertIsNone(response.data)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_with_non_existing_id(self):
        url = self.get_url(1000)
        response = client.delete(url)

        self.assertEqual("Unable to find wishlist product with id 1000", str(response.data["message"]))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    @patch('product_service.views.cache')
    def test_delete_with_delete_cached_data(self, mock_cache):
        mock_cache.has_key.return_value = True

        url = self.get_url(self.wishlist.id)
        response = client.delete(url)

        self.assertIsNone(response.data)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        mock_cache.delete.assert_called_once()
