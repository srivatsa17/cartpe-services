from django.test import TestCase
from unittest.mock import patch, Mock
from auth_service.email import send_verification_email

class SendVerificationEmailTest(TestCase):
    """ Test module for send_verification_email method """

    def setUp(self):
        self.user_email = "testuser@example.com"

    @patch("auth_service.email.EmailMultiAlternatives.send")
    def test_send_verification_email_success(self, mock_send):
        user = Mock()
        user.pk = 123

        with patch("auth_service.email.User.objects.filter") as mock_user_filter, \
            patch("auth_service.email.User.objects.get") as mock_user_get, \
            patch("auth_service.email.render_to_string") as mock_render_to_string:

            # Mock the filter method to return True, indicating the user exists
            mock_user_filter.return_value.exists.return_value = True

            # Mock the get method to return the user
            mock_user_get.return_value = user

            # Mock the render_to_string method to return the HTML content
            mock_render_to_string.return_value = "<html><body>Verification Email</body></html>"

            # Call the send_verification_email function
            receivedResponse = send_verification_email(self.user_email)

            # Assert that the filter and get methods were called with the correct email
            mock_user_filter.assert_called_once_with(email=self.user_email)
            mock_user_get.assert_called_once_with(email=self.user_email)

            # Assert that the send method of EmailMultiAlternatives was called
            mock_send.assert_called_once()

            # Assert the expected return value
            expectedResponse = { "status" : 200 }
            self.assertEqual(receivedResponse, expectedResponse)

    @patch("auth_service.email.EmailMultiAlternatives")
    def test_send_verification_email_failure(self, mock_email_class):
        user = Mock()
        user.pk = 123

        mock_email_instance = mock_email_class.return_value
        mock_send = mock_email_instance.send
        mock_send.side_effect = Exception("Email sending failed")

        with patch("auth_service.email.User.objects.filter") as mock_filter, \
            patch("auth_service.email.User.objects.get") as mock_get, \
            patch("auth_service.email.render_to_string") as mock_render_to_string:

            # Mock the filter method to return True, indicating the user exists
            mock_filter.return_value.exists.return_value = True

            # Mock the get method to return the user
            mock_get.return_value = user

            # Mock the render_to_string method to return the HTML content
            mock_render_to_string.return_value = "<html><body>Verification Email</body></html>"

            # Call the send_verification_email function
            receivedResponse = send_verification_email(self.user_email)

            # Assert that the filter and get methods were called with the correct email
            mock_filter.assert_called_once_with(email=self.user_email)
            mock_get.assert_called_once_with(email=self.user_email)

            # Assert that the EmailMultiAlternatives constructor was called with the correct arguments
            mock_email_class.assert_called_once_with(
                subject="Verify your Email",
                body="Verification Email",
                from_email="CartPe <cartpe.site@gmail.com>",
                to=[self.user_email]
            )

            # Assert that the send method of EmailMultiAlternatives was called
            mock_send.assert_called_once()

            # Assert the expected return value
            expectedResponse = { "status": 400, "error": "Email sending failed" }
            self.assertEqual(receivedResponse, expectedResponse)

    @patch("auth_service.email.EmailMultiAlternatives.send")
    def test_send_verification_email_failure_with_non_existing_user(self, mock_send):
        with patch("auth_service.email.User.objects.filter") as mock_user_filter:
            # Mock the filter method to return False, indicating the user does not exist
            mock_user_filter.return_value.exists.return_value = False

            # Call the send_verification_email function
            receivedResponse = send_verification_email(self.user_email)

            # Assert that the filter method was called with the correct email
            mock_user_filter.assert_called_once_with(email=self.user_email)

            # Assert that the send method of EmailMultiAlternatives was not called
            mock_send.assert_not_called()

            # Assert the expected return value
            expectedResponse = { "status": 400 }
            self.assertEqual(receivedResponse, expectedResponse)
