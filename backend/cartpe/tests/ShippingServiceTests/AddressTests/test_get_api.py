from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from auth_service.models import User
from shipping_service.models import Country, Address
from shipping_service.serializers import AddressSerializer

# Initialize the APIClient app
client = APIClient()


class GetAllAddressTest(APITestCase):
    """Test module for GET request for AddressAPIView API"""

    def get_url(self):
        url = reverse("address")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        self.country = Country.objects.create(name="India")
        self.address = Address.objects.create(
            building="abc",
            area="def",
            city="pqr",
            state="xyz",
            country=self.country,
            pin_code="123244",
        )

    def test_get_with_valid_data(self):
        url = self.get_url()
        response = client.get(url)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
