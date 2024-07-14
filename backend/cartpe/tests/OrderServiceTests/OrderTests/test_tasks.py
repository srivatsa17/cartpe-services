from django.test import TestCase
from unittest.mock import patch
from order_service.tasks import send_order_confirmation_email_task


class SendOrderConfirmationEmailTaskTest(TestCase):
    """Test module for send_order_confirmation_email_task method"""

    def setUp(self):
        self.user_email = "testuser@example.com"

        # Only required field is email, so sending only that in test case.
        self.order_data = {"user": self.user_email}

    @patch("order_service.tasks.send_order_confirmation_email")
    def test_send_order_confirmation_email_task_success(self, mock_send_order_confirmation_email):
        # Mock the delay method of send_order_confirmation_email to return a successful response
        mock_send_order_confirmation_email.return_value = {"status": 200}
        expectedResponse = f"Successfully sent order confirmation email to {self.user_email}"

        # Call the send_order_confirmation_email
        receivedResponse = send_order_confirmation_email_task(self.order_data)

        # Assert that the delay method of send_verification_email was called with the correct email
        mock_send_order_confirmation_email.assert_called_once_with(order_data=self.order_data)
        self.assertEqual(receivedResponse, expectedResponse)

    @patch("order_service.tasks.send_order_confirmation_email")
    def test_send_order_confirmation_email_task_failure(self, mock_send_order_confirmation_email):
        # Mock the send_order_confirmation_email function to return a failure response
        mock_send_order_confirmation_email.return_value = {"status": 400}
        expectedResponse = "Order confirmation email was not sent"

        # Call the send_order_confirmation_email
        receivedResponse = send_order_confirmation_email_task(self.order_data)

        # Assert that the send_order_confirmation_email function was called with the correct email
        mock_send_order_confirmation_email.assert_called_once_with(order_data=self.order_data)
        self.assertEqual(receivedResponse, expectedResponse)
