from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from auth_service.models import User

CONTENT_TYPE = 'application/json'

# Initialize the APIClient app
client = APIClient()

class PostCountryTest(APITestCase):
    """ Test module for POST request for BrandAPIView API """

    def get_url(self):
        url = reverse('country')
        return url

    def setUp(self) -> None:
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.validData = { "name" : "India" }
        self.dataWithExistingName = self.validData

    def test_with_valid_data(self) -> None:
        expectedStatusCode = status.HTTP_201_CREATED

        url = self.get_url()
        data = json.dumps(self.validData)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_name(self) -> None:
        expectedResponse = "This field is required."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({})
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['name'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_same_name(self) -> None:
        expectedResponse = "Country '%s' already exists and cannot be created again." % self.validData['name']
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps(self.validData)
        client.post(url, data = data, content_type = CONTENT_TYPE)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['message'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)