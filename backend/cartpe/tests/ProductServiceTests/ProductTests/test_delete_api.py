from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product
from auth_service.models import User

# Initialize the APIClient app
client = APIClient()

class DeleteProductByIdTest(APITestCase):
    """ Test module for DELETE request for ProductByIdAPIView API """

    def get_url(self, product_id):
        url = reverse("product_by_id", kwargs = { "id": product_id })
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.pixel = Product.objects.create(name = "pixel 7", description = "good product", price = 50000, stock_count = 10)

    def test_delete_with_existing_id(self):
        url = self.get_url(self.pixel.id)
        response = client.delete(url)

        self.assertIsNone(response.data)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_with_non_existing_id(self):
        url = self.get_url(1000)
        response = client.delete(url)

        self.assertEqual("Unable to find product with id 1000", response.data["message"])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
