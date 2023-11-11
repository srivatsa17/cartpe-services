from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from shipping_service.models import Country
from auth_service.models import User

CONTENT_TYPE = 'application/json'

# Initialize the APIClient app
client = APIClient()

class PostUserAddressTest(APITestCase):
    """ Test module for POST request for UserAddressAPIView API """

    def get_url(self):
        url = reverse('user_address')
        return url

    def setUp(self) -> None:
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.country = Country.objects.create(name = "India")
        self.validData = {
            "name": "abc",
            "alternate_phone": "1234567890",
            "type": "Home",
            "is_default": True,
            "address": {
                "line1" : "abc",
                "line2" : "def",
                "city" : "pqr",
                "state" : "xyz",
                "country" : "India",
                "pin_code" : "123244"
            }
        }

    def test_with_valid_data(self) -> None:
        expectedStatusCode = status.HTTP_201_CREATED

        url = self.get_url()
        data = json.dumps(self.validData)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_existing_default_address(self) -> None:
        expectedStatusCode = status.HTTP_201_CREATED

        url = self.get_url()
        data = json.dumps(self.validData)
        client.post(url, data = data, content_type = CONTENT_TYPE)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        response1 = client.get(url)

        self.assertEqual(response1.data[0]['is_default'], False)
        self.assertEqual(response1.data[1]['is_default'], True)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_data(self) -> None:
        expectedResponse = "This field is required."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({})
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(response.data['name'][0], expectedResponse)
        self.assertEqual(response.data['alternate_phone'][0], expectedResponse)
        self.assertEqual(response.data['type'][0], expectedResponse)
        self.assertEqual(response.data['is_default'][0], expectedResponse)
        self.assertEqual(response.data['address'][0], expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)