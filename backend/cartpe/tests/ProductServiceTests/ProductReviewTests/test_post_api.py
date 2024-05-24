from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product
from auth_service.models import User
import json

CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()

class PostProductReviewTest(APITestCase):
    """ Test module for POST request for ProductReviewAPIView API """

    def get_url(self, product_id):
        url = reverse("product_review", kwargs = { "product_id": product_id })
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.product = Product.objects.create(name = "iphone 13", description = "ok product")

    def test_post_with_valid_data(self):
        url = self.get_url(self.product.id)
        data = json.dumps({
            "product": self.product.id,
            "headline": "Extraordinary product",
            "rating": 5
        })
        response = client.post(url, data=data, content_type=CONTENT_TYPE)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post_with_invalid_data(self):
        url = self.get_url(self.product.id)
        response = client.post(
            url, data=json.dumps({ "headline": "Extraordinary product" }), content_type=CONTENT_TYPE
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_with_non_existing_id(self):
        url = self.get_url(1000)
        response = client.post(
            url, data=json.dumps({ "headline": "Extraordinary product" }), content_type=CONTENT_TYPE
        )

        self.assertEqual("Unable to find product with id 1000", str(response.data["message"]))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
