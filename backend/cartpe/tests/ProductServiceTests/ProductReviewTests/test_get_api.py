from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, ProductReview
from auth_service.models import User

# Initialize the APIClient app
client = APIClient()

class GetProductReviewByIdTest(APITestCase):
    """ Test module for GET request forProductReviewByIdAPIView API """

    def get_url(self, product_review_id):
        url = reverse("product_review_by_id", kwargs = { "id" : product_review_id })
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.product = Product.objects.create(name = "iphone 13", description = "ok product")
        self.product_review = ProductReview.objects.create(
            product = self.product, user = self.user, headline = "Amazing product", rating = 5
        )

    def test_get_with_valid_id(self):
        url = self.get_url(self.product_review.id)
        response = client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data)

    def test_get_with_non_existing_id(self):
        url = self.get_url(1000)
        response = client.get(url)

        self.assertEqual("Unable to find product review with id 1000", str(response.data["message"]))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
