from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, ProductReview
from auth_service.models import User
import json

CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()


class UpdateProductReviewTest(APITestCase):
    """Test module for PATCH request for ProductReviewByIdAPIView API"""

    def get_url(self, product_id, product_review_id):
        url = reverse(
            "product_review_by_id", kwargs={"product_id": product_id, "id": product_review_id}
        )
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        self.product = Product.objects.create(name="iphone 13", description="ok product")
        self.product_review = ProductReview.objects.create(
            product=self.product, user=self.user, headline="Amazing product", rating=5
        )

    def test_update_with_valid_data(self):
        url = self.get_url(self.product.id, self.product_review.id)
        data = json.dumps({"headline": "Extraordinary product"})
        response = client.patch(url, data=data, content_type=CONTENT_TYPE)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_update_with_invalid_data(self):
        url = self.get_url(self.product.id, self.product_review.id)
        data = json.dumps({"rating": 10})
        response = client.patch(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_with_non_existing_id(self):
        url = self.get_url(self.product.id, 1000)
        data = json.dumps({"headline": "Extraordinary product"})
        response = client.patch(url, data=data, content_type=CONTENT_TYPE)

        self.assertEqual(
            f"Unable to find review with id 1000 for product {self.product.id}",
            str(response.data["message"]),
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
