from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, ProductVariant
from auth_service.models import User

# Initialize the APIClient app
client = APIClient()

class GetAllProductsTest(APITestCase):
    """ Test module for GET request for ProductAPIView API """

    def get_url(self):
        url = reverse("products")
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

    def test_get_with_valid_data(self):
        url = self.get_url()
        response = client.get(url)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

class GetProductByIdTest(APITestCase):
    """ Test module for GET request for ProductByIdAPIView API """

    def get_url(self, product_id):
        url = reverse("product_by_id", kwargs = { "id" : product_id })
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

    def test_get_with_valid_id(self):
        url = self.get_url(self.product1.id)
        response = client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data)

    def test_get_with_non_existing_id(self):
        url = self.get_url(1000)
        response = client.get(url)

        self.assertEqual("Unable to find product with id 1000", response.data["message"])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
