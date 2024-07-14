from django.test import TestCase
from unittest.mock import patch, Mock
from order_service.email import send_order_confirmation_email


class SendOrderConfirmationEmailTest(TestCase):
    """Test module for send_order_confirmation_email method"""

    def setUp(self):
        self.user_email = "testuser@example.com"

        # Only required field is email, so sending only that in test case.
        self.order_data = {"user": self.user_email}

    @patch("order_service.email.EmailMultiAlternatives.send")
    def test_send_order_confirmation_email_success(self, mock_send):
        user = Mock()
        user.pk = 123

        with patch("order_service.email.User.objects.filter") as mock_user_filter, patch(
            "order_service.email.render_to_string"
        ) as mock_render_to_string:

            # Mock the render_to_string method to return the HTML content
            mock_render_to_string.return_value = (
                "<html><body>Order Confirmation Email</body></html>"
            )

            # Call the send_order_confirmation_email function
            receivedResponse = send_order_confirmation_email(self.order_data)

            # Assert that the filter and get methods were called with the correct email
            mock_user_filter.assert_called_once_with(email=self.user_email)

            # Assert that the send method of EmailMultiAlternatives was called
            mock_send.assert_called_once()

            # Assert the expected return value
            expectedResponse = {"status": 200}
            self.assertEqual(receivedResponse, expectedResponse)

    @patch("order_service.email.EmailMultiAlternatives")
    def test_send_order_confirmation_email_exception(self, mock_email_class):
        user = Mock()
        user.pk = 123

        mock_email_instance = mock_email_class.return_value
        mock_send = mock_email_instance.send
        mock_send.side_effect = Exception("Email sending failed")

        with patch("order_service.email.User.objects.filter") as mock_user_filter, patch(
            "order_service.email.render_to_string"
        ) as mock_render_to_string:

            # Mock the render_to_string method to return the HTML content
            mock_render_to_string.return_value = (
                "<html><body>Order Confirmation Email</body></html>"
            )

            # Call the send_order_confirmation_email function
            receivedResponse = send_order_confirmation_email(self.order_data)

            # Assert that the filter methods were called with the correct email
            mock_user_filter.assert_called_once_with(email=self.user_email)

            # Assert that the EmailMultiAlternatives constructor was called with the correct arguments
            mock_email_class.assert_called_once_with(
                subject="CartPe Order Confirmation",
                body="Order Confirmation Email",
                from_email="CartPe <cartpe.site@gmail.com>",
                to=[self.user_email],
            )

            # Assert that the send method of EmailMultiAlternatives was called
            mock_send.assert_called_once()

            # Assert the expected return value
            expectedResponse = {"status": 400, "error": "Email sending failed"}
            self.assertEqual(receivedResponse, expectedResponse)
