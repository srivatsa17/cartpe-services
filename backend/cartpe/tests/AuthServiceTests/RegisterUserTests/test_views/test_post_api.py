from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from auth_service.models import User

CONTENT_TYPE = 'application/json'

# Initialize the APIClient app
client = APIClient()

class PostRegisterUserTest(APITestCase):
    """ Test module for POST request for RegisterAPIView API """

    def get_url(self):
        url = reverse('register')
        return url

    def setUp(self) -> None:
        self.validData = {
            "email" : "testuser@example.com",
            "password" : "testpassword",
            "first_name": "testuser",
            "last_name": "testuser"
        }
        self.invalidData = { "email" : "abc", "password" : "abc" }

    @patch('auth_service.views.send_verification_email_task.delay')
    def test_with_valid_data(self, mock_send_verification_email_task) -> None:
        expectedStatusCode = status.HTTP_201_CREATED

        url = self.get_url()
        data = json.dumps(self.validData)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(receivedStatusCode, expectedStatusCode)

        # Assert that the send_verification_email function was called with the correct email
        mock_send_verification_email_task.assert_called_once_with(user_email=self.validData['email'])

    @patch('auth_service.views.send_verification_email_task.delay')
    def test_with_invalid_data(self, mock_send_verification_email_task) -> None:
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps(self.invalidData)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(receivedStatusCode, expectedStatusCode)
        mock_send_verification_email_task.assert_not_called()

    @patch('auth_service.views.send_verification_email_task.delay')
    def test_with_existing_email(self, mock_send_verification_email_task) -> None:
        user = User.objects.create(email = self.validData['email'], password = "abcdefgh")
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps(self.validData)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(receivedStatusCode, expectedStatusCode)
        mock_send_verification_email_task.assert_not_called()