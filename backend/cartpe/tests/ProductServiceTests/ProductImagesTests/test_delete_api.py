from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, Image
from auth_service.models import User

# Global variables
SAMPLE_IMAGE_1 = "https://cartpe.s3.ap-south-1.amazonaws.com/Products/Canon+80D/canon_80D_image_1.webp"

# Initialize the APIClient app
client = APIClient()

class DeleteImageTest(APITestCase):
    """ Test module for DELETE request for ProductImageByIdAPIView API """

    def get_url(self, imageId):
        url = reverse("image_by_id", kwargs = {"id" : imageId})
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.product = Product.objects.create(name = "Canon 80D", description = "good product", price = 50000, stock_count = 10)
        self.image1 = Image.objects.create(image=SAMPLE_IMAGE_1, is_featured=True, product=self.product)

    def test_delete_with_existing_id(self):
        url = self.get_url(self.image1.id)
        response = client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertIsNone(response.data)

    def test_delete_with_nonexisting_id(self):
        url = self.get_url(1000)
        response = client.delete(url)

        self.assertEqual("Unable to find image with id 1000", str(response.data["message"]))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
