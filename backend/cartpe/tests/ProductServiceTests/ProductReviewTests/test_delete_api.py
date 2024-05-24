from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, ProductReview
from auth_service.models import User

# Initialize the APIClient app
client = APIClient()

class DeleteProductReviewByIdTest(APITestCase):
    """ Test module for DELETE request for ProductReviewByIdAPIView API """

    def get_url(self, product_id, product_review_id):
        url = reverse("product_review_by_id", kwargs = { "product_id": product_id, "id": product_review_id })
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.product = Product.objects.create(name = "iphone 13", description = "ok product")
        self.product_review = ProductReview.objects.create(
            product = self.product, user = self.user, headline = "Amazing product", rating = 5
        )

    def test_delete_with_existing_id(self):
        url = self.get_url(self.product.id, self.product_review.id)
        response = client.delete(url)

        self.assertIsNone(response.data)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_with_non_existing_id(self):
        url = self.get_url(self.product.id, 1000)
        response = client.delete(url)

        self.assertEqual(
            f"Unable to find review with id 1000 for product {self.product.id}", str(response.data["message"])
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
