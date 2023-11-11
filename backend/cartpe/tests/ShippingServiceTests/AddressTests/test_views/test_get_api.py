from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from auth_service.models import User
from shipping_service.models import Country, Address
from shipping_service.serializers import AddressSerializer

# Initialize the APIClient app
client = APIClient()

class GetAllAddressTest(APITestCase):
    """ Test module for GET request for AddressAPIView API """

    def get_url(self):
        url = reverse('address')
        return url

    def setUp(self) -> None:
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.country = Country.objects.create(name = "India")
        self.address = Address.objects.create(
            line1 = "abc", line2 = "def", city = "pqr", state = "xyz", country = self.country,
            pin_code = "123244"
        )

    def test_valid_data(self) -> None:
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many = True)
        expectedResponse = serializer.data
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url()
        response = client.get(url)
        receivedResponse = response.data
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)
