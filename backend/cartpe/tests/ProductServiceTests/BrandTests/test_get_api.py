from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Brand
from product_service.serializers import BrandSerializer
from auth_service.models import User

# Initialize the APIClient app
client = APIClient()


class GetAllBrandsTest(APITestCase):
    """Test module for GET request for BrandAPIView API"""

    def get_url(self):
        url = reverse("brands")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        Brand.objects.create(name="Apple", description="ok brand")
        Brand.objects.create(name="Google", description="good brand")

    def test_get_all_brands(self):
        url = self.get_url()
        response = client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data)


class GetBrandByIdTest(APITestCase):
    """Test module for GET request for BrandByIdAPIView API"""

    def get_url(self, brand_id):
        url = reverse("brand_by_id", kwargs={"id": brand_id})
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        self.apple = Brand.objects.create(name="apple", description="ok brand")
        self.google = Brand.objects.create(name="google", description="good brand")

    def test_get_brand_with_valid_id(self):
        url = self.get_url(self.google.id)
        response = client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data)

    def test_get_brand_with_invalid_id(self):
        url = self.get_url(1000)
        response = client.get(url)

        self.assertEqual("Unable to find brand with id 1000", response.data["message"])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
