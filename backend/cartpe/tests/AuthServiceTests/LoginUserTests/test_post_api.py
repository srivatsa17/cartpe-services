from django.test import Client
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APITestCase
from rest_framework import status
import json
from auth_service.models import User

CONTENT_TYPE = 'application/json'

# Initialize the APIClient app
client = Client()

class PostLoginUserTest(APITestCase):
    """ Test module for POST request for LoginAPIView API """

    def get_url(self):
        url = reverse('login')
        return url

    def setUp(self) -> None:
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")

    def test_login_success(self) -> None:
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url()
        data = json.dumps({ "email" : "testuser@example.com", "password" : "abcdef" })
        self.user.is_verified = True
        self.user.save()

        response = self.client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(expectedStatusCode, receivedStatusCode)
        self.assertTrue(response.data['tokens']['access'])
        self.assertTrue(response.data['tokens']['refresh'])

    def test_with_empty_username_password(self) -> None:
        expectedStatusCode = status.HTTP_400_BAD_REQUEST
        expectedResponse = "This field may not be blank."

        url = self.get_url()
        data = json.dumps({ "email" : "", "password" : "" })

        response = self.client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(expectedStatusCode, receivedStatusCode)
        self.assertEqual(response.data['email'][0], expectedResponse)
        self.assertTrue(response.data['password'][0], expectedResponse)

    def test_login_with_non_existing_user(self) -> None:
        expectedStatusCode = status.HTTP_401_UNAUTHORIZED
        expectedResponse = "Please ensure that your credentials are valid and that the user account is enabled."

        url = self.get_url()
        data = json.dumps({ "email" : "nonexistinguser@example.com", "password" : "abcdef" })
        response = self.client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = response.data['detail']

        self.assertEqual(expectedStatusCode, receivedStatusCode)
        self.assertEqual(expectedResponse, receivedResponse)

    def test_login_with_invalid_credentials(self) -> None:
        expectedStatusCode = status.HTTP_401_UNAUTHORIZED
        expectedResponse = "Please ensure that your credentials are valid and that the user account is enabled."

        url = self.get_url()
        data = json.dumps({ "email" : "testuser@example.com", "password" : "qwerty" })
        response = self.client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = response.data['detail']

        self.assertEqual(expectedStatusCode, receivedStatusCode)
        self.assertEqual(expectedResponse, receivedResponse)

    def test_login_with_non_verified_user(self) -> None:
        expectedStatusCode = status.HTTP_401_UNAUTHORIZED
        expectedResponse = "Please ensure that your email is verified."

        url = self.get_url()
        data = json.dumps({ "email" : "testuser@example.com", "password" : "abcdef" })

        response = self.client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = response.data['detail']

        self.assertEqual(expectedStatusCode, receivedStatusCode)
        self.assertEqual(expectedResponse, receivedResponse)