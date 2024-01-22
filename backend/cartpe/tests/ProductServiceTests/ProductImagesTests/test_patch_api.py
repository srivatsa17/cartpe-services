import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, Image
from auth_service.models import User

# Global variables
CONTENT_TYPE = "application/json"
SAMPLE_IMAGE_1 = "https://cartpe.s3.ap-south-1.amazonaws.com/Products/Canon+80D/canon_80D_image_1.webp"
SAMPLE_IMAGE_2 = "https://cartpe.s3.ap-south-1.amazonaws.com/Products/Canon+80D/canon_80D_image_2.webp"

# Initialize the APIClient app
client = APIClient()

class UpdateImageTest(APITestCase):
    """ Test module for PATCH request for ProductImageByIdAPIView API """

    def get_url(self, image_id):
        url = reverse("image_by_id", kwargs = { "id" : image_id })
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.product = Product.objects.create(name="Canon 80D", description="good product", price=50000, stock_count=10)
        self.image1 = Image.objects.create(image=SAMPLE_IMAGE_1, is_featured=True, product=self.product)

    def test_update_with_valid_image_id(self):
        url = self.get_url(self.image1.id)
        data = json.dumps({ "image" : SAMPLE_IMAGE_2, "is_featured" : False })
        response = client.patch(url, data, content_type=CONTENT_TYPE)

        self.assertIn(SAMPLE_IMAGE_2, response.data["image"])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_update_with_invalid_image_id(self):
        url = self.get_url(1000)
        data = json.dumps({ "image" : SAMPLE_IMAGE_1, "is_featured" : False })
        response = client.patch(url, data, content_type=CONTENT_TYPE)

        self.assertEqual("Unable to find image with id 1000", response.data["message"])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_update_with_empty_image_url(self):
        url = self.get_url(self.image1.id)
        data = json.dumps({ "image" : "", "is_featured" : True })
        response = client.patch(url, data, content_type=CONTENT_TYPE)

        self.assertEqual("This field may not be blank.", str(response.data["image"][0]))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_with_true_value_for_is_featured_field(self):
        url = self.get_url(self.image1.id)
        data = json.dumps({ "image" : SAMPLE_IMAGE_1, "is_featured" : True })
        response = client.patch(url, data, content_type=CONTENT_TYPE)

        self.assertEqual(
            "is_featured=True cannot be set as there exists a featured image for productId " + str(self.product.id),
            str(response.data["message"][0])
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
