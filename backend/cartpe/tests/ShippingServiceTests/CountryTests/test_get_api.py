from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from auth_service.models import User
from shipping_service.models import Country

# Initialize the APIClient app
client = APIClient()


class GetAllCountriesTest(APITestCase):
    """Test module for GET request for CountryAPIView API"""

    def get_url(self):
        url = reverse("country")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        Country.objects.create(name="India")

    def test_get_with_valid_data(self):
        url = self.get_url()
        response = client.get(url)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
