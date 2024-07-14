from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Brand
from auth_service.models import User

# Initialize the APIClient app
client = APIClient()


class DeleteBrandByIdTest(APITestCase):
    """Test module for DELETE request for BrandByIdAPIView API"""

    def get_url(self, brand_id):
        url = reverse("brand_by_id", kwargs={"id": brand_id})
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        self.google = Brand.objects.create(name="google", description="good brand")

    def test_delete_with_existing_id(self):
        url = self.get_url(self.google.id)
        response = client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_with_non_existing_id(self):
        url = self.get_url(1000)
        response = client.delete(url)

        self.assertEqual("Unable to find brand with id 1000", response.data["message"])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
