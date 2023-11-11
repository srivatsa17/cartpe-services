from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from auth_service.models import User
from shipping_service.models import Country
from shipping_service.serializers import CountrySerializer

# Initialize the APIClient app
client = APIClient()

class GetAllCountriesTest(APITestCase):
    """ Test module for GET request for CountryAPIView API """

    def get_url(self):
        url = reverse('country')
        return url

    def setUp(self) -> None:
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        Country.objects.create(name = "India")

    def test_valid_data(self) -> None:
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many = True)
        expectedResponse = serializer.data
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url()
        response = client.get(url)
        receivedResponse = response.data
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)
