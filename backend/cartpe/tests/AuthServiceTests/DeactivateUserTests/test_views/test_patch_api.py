from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import json
from auth_service.models import User

CONTENT_TYPE = 'application/json'

# Initialize the APIClient app
client = APIClient()

class DeactivateUserTests(APITestCase):
    """ Test module for PATCH request to DeactivateUserAPIView api """

    def get_url(self):
        url = reverse('deactivate')
        return url

    def setUp(self) -> None:
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        self.refresh_token = str(RefreshToken.for_user(self.user))
        self.access_token = str(RefreshToken.for_user(self.user).access_token)

    def test_success(self) -> None:
        expectedStatusCode = status.HTTP_200_OK
        expectedResponse = "Account deactivated successfully."

        url = self.get_url()
        data = json.dumps({ "refresh_token" : self.refresh_token })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = response.data['message']

        self.assertEqual(expectedStatusCode, receivedStatusCode)
        self.assertEqual(expectedResponse, receivedResponse)

    def test_with_no_token(self) -> None:
        expectedStatusCode = status.HTTP_401_UNAUTHORIZED

        url = self.get_url()
        data = json.dumps({})
        response = self.client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(expectedStatusCode, receivedStatusCode)

    def test_failure(self) -> None:
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(expectedStatusCode, receivedStatusCode)