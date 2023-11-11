from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from shipping_service.models import Country
from auth_service.models import User

CONTENT_TYPE = 'application/json'

# Initialize the APIClient app
client = APIClient()

class PostAddressTest(APITestCase):
    """ Test module for POST request for AddressAPIView API """

    def get_url(self):
        url = reverse('address')
        return url

    def setUp(self) -> None:
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.country = Country.objects.create(name = "India")
        self.validData = {
            "line1" : "abc",
            "line2" : "def",
            "city" : "pqr",
            "state" : "xyz",
            "country" : "India",
            "pin_code" : "123244"
        }

    def test_with_valid_data(self) -> None:
        expectedStatusCode = status.HTTP_201_CREATED

        url = self.get_url()
        data = json.dumps(self.validData)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_data(self) -> None:
        expectedResponse = "This field is required."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({})
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(response.data['line1'][0], expectedResponse)
        self.assertEqual(response.data['line2'][0], expectedResponse)
        self.assertEqual(response.data['city'][0], expectedResponse)
        self.assertEqual(response.data['state'][0], expectedResponse)
        self.assertEqual(response.data['country'][0], expectedResponse)
        self.assertEqual(response.data['pin_code'][0], expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)