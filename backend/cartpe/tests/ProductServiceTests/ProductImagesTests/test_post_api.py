import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, Image
from auth_service.models import User

# Global variables
CONTENT_TYPE = "application/json"
SAMPLE_IMAGE_1 = "https://cartpe.s3.ap-south-1.amazonaws.com/Products/Canon+80D/canon_80D_image_1.webp"

# Initialize the APIClient app
client = APIClient()

class PostImageTest(APITestCase):
    """ Test module for POST request for ProductImageAPIView API """

    def get_url(self, param_key=None, param_value=None):
        if param_key is None and param_value is None:
            url = reverse("images")
        else:
            url = reverse("images") + f"?{param_key}={param_value}"
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.product = Product.objects.create(name="Canon 80D", description="good product", price=50000, stock_count=10)

    def test_post_with_valid_data(self):
        url = self.get_url("product", self.product.id)
        data = json.dumps({ "image" : SAMPLE_IMAGE_1, "is_featured" : True })
        response = client.post(url, data, content_type = CONTENT_TYPE)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post_with_missing_fields(self):
        url = self.get_url("product", self.product.id)
        data = json.dumps({})
        response = client.post(url, data, content_type = CONTENT_TYPE)

        self.assertEqual("This field is required.", str(response.data["image"][0]))
        self.assertEqual("This field is required.", str(response.data["is_featured"][0]))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_with_invalid_image(self):
        url = self.get_url("product", self.product.id)
        data = json.dumps({ "image" : "", "is_featured" : True })
        response = client.post(url, data, content_type = CONTENT_TYPE)

        self.assertEqual("This field may not be blank.", str(response.data["image"][0]))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_with_true_value_for_is_featured_field(self):
        self.imageObj = Image.objects.create(image=SAMPLE_IMAGE_1, is_featured=True, product=self.product)

        url = self.get_url("product", self.product.id)
        data = json.dumps({ "image" : SAMPLE_IMAGE_1, "is_featured" : True })
        response = client.post(url, data, content_type = CONTENT_TYPE)

        self.assertEqual(
            "is_featured=True cannot be set as there exists a featured image for productId " + str(self.product.id),
            str(response.data["message"][0])
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_with_empty_params(self):
        url = self.get_url()
        data = json.dumps({ "image" : SAMPLE_IMAGE_1, "is_featured" : True })
        response = client.post(url, data, content_type = CONTENT_TYPE)

        self.assertEqual("Please make sure query params are sent in the format ?product=<id>.", response.data["message"])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_with_characters_in_params(self):
        url = self.get_url("product", "abc")
        data = json.dumps({ "image" : SAMPLE_IMAGE_1, "is_featured" : True })
        response = client.post(url, data, content_type = CONTENT_TYPE)

        self.assertEqual("Please enter a valid integer for product id.", response.data["message"])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_with_empty_value_in_params(self):
        url = self.get_url("product", "")
        data = json.dumps({ "image" : SAMPLE_IMAGE_1, "is_featured" : True })
        response = client.post(url, data, content_type = CONTENT_TYPE)

        self.assertEqual("Please enter a valid integer for product id.", response.data["message"])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_with_non_existing_product_in_params(self):
        url = self.get_url("product", 1000)
        data = json.dumps({ "image" : SAMPLE_IMAGE_1, "is_featured" : True })
        response = client.post(url, data, content_type = CONTENT_TYPE)

        self.assertEqual("Unable to find product with id 1000", str(response.data["message"]))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
