from django.test import TestCase
from unittest.mock import patch
from auth_service.tasks import send_verification_email_task

class SendVerificationEmailTaskTest(TestCase):
    """ Test module for send_verification_email_task method """

    def setUp(self):
        self.user_email = "testuser@example.com"

    @patch("auth_service.tasks.send_verification_email")
    def test_send_verification_email_task_success(self, mock_send_verification_email):
        # Mock the delay method of send_verification_email to return a successful response
        mock_send_verification_email.return_value = { "status": 200 }
        expectedResponse = f"Successfully sent verification email to {self.user_email}"

        # Call the send_verification_email_task
        receivedResponse = send_verification_email_task(self.user_email)

        # Assert that the delay method of send_verification_email was called with the correct email
        mock_send_verification_email.assert_called_once_with(user_email=self.user_email)
        self.assertEqual(receivedResponse, expectedResponse)

    @patch("auth_service.tasks.send_verification_email")
    def test_send_verification_email_task_failure(self, mock_send_verification_email):
        # Mock the send_verification_email function to return a failure response
        mock_send_verification_email.return_value = { "status": 400 }
        expectedResponse = "Verification email was not sent"

        # Call the send_verification_email_task
        receivedResponse = send_verification_email_task(self.user_email)

        # Assert that the send_verification_email function was called with the correct email
        mock_send_verification_email.assert_called_once_with(user_email=self.user_email)
        self.assertEqual(receivedResponse, expectedResponse)