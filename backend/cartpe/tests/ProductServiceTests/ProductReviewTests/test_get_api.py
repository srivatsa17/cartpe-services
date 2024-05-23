from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, ProductReview
from auth_service.models import User

# Initialize the APIClient app
client = APIClient()

class GetProductReviewTest(APITestCase):
    """ Test module for GET request for ProductReviewAPIView API """

    def get_url(self, product_id):
        url = reverse("product_review", kwargs = { "product_id": product_id })
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.product = Product.objects.create(name = "iphone 13", description = "ok product")
        self.product_review = ProductReview.objects.create(
            product = self.product, user = self.user, headline = "Amazing product", rating = 5
        )

    def test_get_with_valid_id(self):
        url = self.get_url(self.product.id)
        response = client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data)

    def test_get_with_non_existing_id(self):
        url = self.get_url(1000)
        response = client.get(url)

        self.assertEqual("Unable to find product with id 1000", str(response.data["message"]))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

class GetProductReviewByIdTest(APITestCase):
    """ Test module for GET request for ProductReviewByIdAPIView API """

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

    def test_get_with_valid_id(self):
        url = self.get_url(self.product.id, self.product_review.id)
        response = client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data)

    def test_get_with_non_existing_id(self):
        url = self.get_url(self.product.id, 1000)
        response = client.get(url)

        self.assertEqual(
            f"Unable to find review with id 1000 for product {self.product.id}", str(response.data["message"])
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

class GetProductRatingTest(APITestCase):
    """ Test module for GET request for ProductRatingAPIView API """

    def get_url(self, product_id):
        url = reverse("product_rating", kwargs = { "product_id": product_id })
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.product = Product.objects.create(name = "iphone 13", description = "ok product")

    def test_get_with_valid_id(self):
        url = self.get_url(self.product.id)
        # First check for 0 rating with no reviews created yet.
        response = client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data)

        self.product_review = ProductReview.objects.create(
            product = self.product, user = self.user, headline = "Amazing product", rating = 5
        )

        # Now, check with the review created.
        response = client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data)

    def test_get_with_non_existing_id(self):
        url = self.get_url(1000)
        response = client.get(url)

        self.assertEqual("Unable to find product with id 1000", str(response.data["message"]))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)