from django.test import Client
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.test import APITestCase
from rest_framework import status
import json
from auth_service.models import User
from auth_service.token import account_activation_token

CONTENT_TYPE = 'application/json'

# Initialize the APIClient app
client = Client()

class VerifyUserEmailTest(APITestCase):
    """ Test module for PATCH request for VerifyUserEmailAPIView API """

    def get_url(self):
        url = reverse("verify-email")
        return url

    def setUp(self) -> None:
        self.user = User.objects.create(email = "testuser@example.com", password = "abcdefgh")

    def test_success(self) -> None:
        expectedResponse = "Email Verified Successfully"
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url()
        data = json.dumps({
            "uidb64" : urlsafe_base64_encode(force_bytes(self.user.pk)),
            "token" : account_activation_token.make_token(self.user)
        })

        response = self.client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertTrue(response.data['isEmailVerified'])
        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_invalid_uidb64(self) -> None:
        expectedResponse = "Error occurred while decoding base64 user id"
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({
            "uidb64" : "abcd123",
            "token" : account_activation_token.make_token(self.user)
        })

        response = self.client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['message'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_invalid_decoded_pk(self) -> None:
        expectedResponse = "Invalid type received for user id"
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({
            "uidb64" : urlsafe_base64_encode(force_bytes(self.user.pk)) + "a",
            "token" : account_activation_token.make_token(self.user)
        })

        response = self.client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['message'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_non_existing_user(self) -> None:
        expectedResponse = "Unable to find user"
        expectedStatusCode = status.HTTP_400_BAD_REQUEST
        newUserPK = 123

        url = self.get_url()
        data = json.dumps({
            "uidb64" : urlsafe_base64_encode(force_bytes(newUserPK)),
            "token" : account_activation_token.make_token(self.user)
        })

        response = self.client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['message'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_invalid_token(self) -> None:
        expectedResponse = "Invalid or expired token"
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({
            "uidb64" : urlsafe_base64_encode(force_bytes(self.user.pk)),
            "token" : "invalid_token"
        })

        response = self.client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['message'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)