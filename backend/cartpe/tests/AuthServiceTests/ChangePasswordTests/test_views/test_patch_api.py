from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import json
from auth_service.models import User

CONTENT_TYPE = 'application/json'

# Initialize the APIClient app
client = APIClient()

class ChangePasswordTests(APITestCase):
    """ Test module for PATCH request to ChangePasswordAPIView api """

    def get_url(self):
        url = reverse('change-password')
        return url

    def setUp(self) -> None:
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        self.refresh_token = str(RefreshToken.for_user(self.user))
        self.access_token = str(RefreshToken.for_user(self.user).access_token)

    def test_success(self) -> None:
        expectedStatusCode = status.HTTP_200_OK
        expectedResponse = "Password updated successfully."

        url = self.get_url()
        data = json.dumps({
            "old_password" : "abcdef",
            "new_password" : "testuser123",
            "confirm_new_password" : "testuser123"
        })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = response.data['message']

        self.assertEqual(expectedStatusCode, receivedStatusCode)
        self.assertEqual(expectedResponse, receivedResponse)

    def test_with_no_token(self) -> None:
        expectedStatusCode = status.HTTP_401_UNAUTHORIZED

        url = self.get_url()
        data = json.dumps({
            "old_password" : "abcdef",
            "new_password" : "testuser123",
            "confirm_new_password" : "testuser123"
        })
        response = self.client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(expectedStatusCode, receivedStatusCode)

    def test_with_empty_body(self) -> None:
        expectedStatusCode = status.HTTP_400_BAD_REQUEST
        expectedResponse = "This field is required."

        url = self.get_url()
        data = json.dumps({})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponseForOldPassword = response.data['old_password'][0]
        receivedResponseForNewPassword = response.data['new_password'][0]
        receivedResponseForConfirmNewPassword = response.data['confirm_new_password'][0]

        self.assertEqual(expectedStatusCode, receivedStatusCode)
        self.assertEqual(expectedResponse, receivedResponseForOldPassword)
        self.assertEqual(expectedResponse, receivedResponseForNewPassword)
        self.assertEqual(expectedResponse, receivedResponseForConfirmNewPassword)

    def test_with_wrong_old_password(self) -> None:
        expectedStatusCode = status.HTTP_400_BAD_REQUEST
        expectedResponse = "Old password is incorrect."

        url = self.get_url()
        data = json.dumps({
            "old_password" : "abcdefg",
            "new_password" : "testuser123",
            "confirm_new_password" : "testuser123"
        })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = response.data['message'][0]

        self.assertEqual(expectedStatusCode, receivedStatusCode)
        self.assertEqual(expectedResponse, receivedResponse)

    def test_with_same_password(self) -> None:
        expectedStatusCode = status.HTTP_400_BAD_REQUEST
        expectedResponse = "New password is same as Old password."

        url = self.get_url()
        data = json.dumps({
            "old_password" : "abcdef",
            "new_password" : "abcdef",
            "confirm_new_password" : "abcdef"
        })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = response.data['message'][0]

        self.assertEqual(expectedStatusCode, receivedStatusCode)
        self.assertEqual(expectedResponse, receivedResponse)

    def test_with_no_alphanumeric_chars(self) -> None:
        expectedStatusCode = status.HTTP_400_BAD_REQUEST
        expectedResponse = "Password should contain alphabets and digits."

        url = self.get_url()
        data = json.dumps({
            "old_password" : "abcdef",
            "new_password" : "testuser",
            "confirm_new_password" : "testuser"
        })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = response.data['message'][0]

        self.assertEqual(expectedStatusCode, receivedStatusCode)
        self.assertEqual(expectedResponse, receivedResponse)

    def test_with_unmatched_new_passwords(self) -> None:
        expectedStatusCode = status.HTTP_400_BAD_REQUEST
        expectedResponse = "New passwords not matching."

        url = self.get_url()
        data = json.dumps({
            "old_password" : "abcdef",
            "new_password" : "testuser123",
            "confirm_new_password" : "testuser12"
        })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = response.data['message'][0]

        self.assertEqual(expectedStatusCode, receivedStatusCode)
        self.assertEqual(expectedResponse, receivedResponse)