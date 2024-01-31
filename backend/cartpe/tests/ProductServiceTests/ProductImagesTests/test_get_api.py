from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, Image
from product_service.serializers import ProductImageSerializer
from auth_service.models import User

# Global variables
SAMPLE_IMAGE_1 = "https://cartpe.s3.ap-south-1.amazonaws.com/Products/Canon+80D/canon_80D_image_1.webp"

# Initialize the APIClient app
client = APIClient()

class GetAllImagesTest(APITestCase):
    """ Test module for GET request for ProductImageAPIView API """

    def get_url(self, paramKey=None, paramValue=None):
        if paramKey is None and paramValue is None:
            url = reverse("images")
        else:
            url = reverse("images") + f"?{paramKey}={paramValue}"
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.product = Product.objects.create(name="Canon 80D", description="good product", price=50000, stock_count=10)
        self.image_instance1 = Image.objects.create(image=SAMPLE_IMAGE_1, is_featured=True, product=self.product)
        self.image_instance2 = Image.objects.create(image=SAMPLE_IMAGE_1, is_featured=False, product=self.product)

    def test_get_with_valid_params(self):
        url = self.get_url("product", self.product.id)
        response = client.get(url)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_with_empty_params(self):
        url = self.get_url()
        response = client.get(url)

        self.assertEqual("Please make sure query params are sent in the format ?product=<id>.", response.data["message"])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_with_characters_in_params(self):
        url = self.get_url("product", "abc")
        response = client.get(url)

        self.assertEqual("Please enter a valid integer for product id.", response.data["message"])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_with_empty_value_in_params(self):
        url = self.get_url("product", "")
        response = client.get(url)

        self.assertEqual("Please enter a valid integer for product id.", response.data["message"])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_with_non_existing_product_in_params(self):
        url = self.get_url("product", 1000)
        response = client.get(url)

        self.assertEqual("Unable to find product with id 1000", response.data["message"])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

class GetImageByIdTest(APITestCase):
    """ Test module for GET request for ProductImageByIdAPIView API """

    def get_url(self, image_id):
        url = reverse("image_by_id", kwargs = { "id" : image_id })
        return url

    def setUp(self):
        self.product = Product.objects.create(name="Canon 80D", description="good product", price=50000, stock_count=10)
        self.image_instance1 = Image.objects.create(image=SAMPLE_IMAGE_1, is_featured=True, product=self.product)
        self.image_instance2 = Image.objects.create(image=SAMPLE_IMAGE_1, is_featured=False, product=self.product)

    def test_get_with_valid_image_id(self):
        url = self.get_url(self.image_instance1.id)
        response = client.get(url)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_with_invalid_image_id(self):
        url = self.get_url(1000)
        response = client.get(url)

        self.assertEqual("Unable to find image with id 1000", str(response.data["message"]))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
