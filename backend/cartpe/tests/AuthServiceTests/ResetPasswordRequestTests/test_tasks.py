from django.test import TestCase
from unittest.mock import patch
from auth_service.models import User
from auth_service.tasks import send_reset_password_email_task

class SendResetPasswordTaskTest(TestCase):
    """ Test module for send_reset_password_email_task method """

    def setUp(self):
        self.user_email = "testuser@example.com"

    @patch("auth_service.tasks.send_reset_password_email_task")
    def test_success(self, mock_send_reset_password_email):
        self.user = User.objects.create_user(
            email = "testuser@example.com", password = "test@123",
            first_name = "test_user", last_name = "test_user"
        )

        # Mock the delay method of send_reset_password_email to return a successful response
        mock_send_reset_password_email.return_value = { "status": 200 }
        expectedResponse = f"Successfully sent reset password email to {self.user_email}"

        # Call the send_reset_password_email_task
        receivedResponse = send_reset_password_email_task(self.user_email)

        self.assertEqual(receivedResponse, expectedResponse)

    @patch("auth_service.tasks.send_reset_password_email_task")
    def test_failure(self, mock_send_reset_password_email):
        # Mock the send_verification_email function to return a failure response
        mock_send_reset_password_email.return_value = { "status": 400 }
        expectedResponse = "Reset password email was not sent."

        # Call the send_verification_email_task
        receivedResponse = send_reset_password_email_task(self.user_email)

        self.assertEqual(receivedResponse, expectedResponse)
