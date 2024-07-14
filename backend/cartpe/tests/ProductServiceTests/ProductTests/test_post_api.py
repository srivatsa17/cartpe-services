from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from product_service.models import Category, Brand
from auth_service.models import User

CONTENT_TYPE = "application/json"
SAMPLE_IMAGE = (
    "https://cartpe.s3.ap-south-1.amazonaws.com/Products/Canon+80D/canon_80D_image_1.webp"
)

# Initialize the APIClient app
client = APIClient()


class PostProductTest(APITestCase):
    """Test module for POST request for ProductAPIView API"""

    def get_url(self):
        url = reverse("products")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="DSLR Cameras")
        self.brand = Brand.objects.create(name="Cannon")
        self.valid_data = {
            "name": "Cannon EOS 80D DSLR Camera",
            "description": "Characterized by versatile imaging specs, the Canon EOS 80D further clarifies itself using a pair of robust focusing systems and an intuitive design",
            "brand": "Cannon",
            "category": "DSLR Cameras",
            "product_variants": [
                {
                    "images": [SAMPLE_IMAGE],
                    "price": 199.99,
                    "discount": 10,
                    "stock_count": 50,
                    "properties": [{"name": "color", "value": "blue"}],
                }
            ],
        }

    def test_post_with_valid_data(self):
        url = self.get_url()
        data = json.dumps(self.valid_data)
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post_with_valid_no_properties_data(self):
        url = self.get_url()
        data = json.dumps(
            {
                "name": "Cannon EOS 80D DSLR Camera",
                "description": "abcd",
                "brand": "Cannon",
                "category": "DSLR Cameras",
                "product_variants": [
                    {
                        "images": [SAMPLE_IMAGE],
                        "price": 199.99,
                        "discount": 10,
                        "stock_count": 50,
                        "properties": [],
                    }
                ],
            }
        )
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post_with_missing_fields(self):
        url = self.get_url()
        data = json.dumps({})
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual("This field is required.", response.data["name"][0])
        self.assertEqual("This field is required.", response.data["description"][0])
        self.assertEqual("This field is required.", response.data["brand"][0])
        self.assertEqual("This field is required.", response.data["category"][0])
        self.assertEqual("This field is required.", response.data["product_variants"][0])

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_with_same_name(self):
        url = self.get_url()
        data = json.dumps(self.valid_data)
        client.post(url, data=data, content_type=CONTENT_TYPE)
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(
            "Product 'Cannon EOS 80D DSLR Camera' already exists and cannot be created again.",
            str(response.data["message"][0]),
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
