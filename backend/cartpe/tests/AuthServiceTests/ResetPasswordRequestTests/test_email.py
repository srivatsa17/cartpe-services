from django.test import TestCase
from unittest.mock import patch, MagicMock
from auth_service.models import User
from auth_service.email import send_reset_password_email
from cartpe import settings

class SendResetPasswordEmailTest(TestCase):
    """ Test module for send_reset_password_email method """

    def setUp(self):
        self.user_email = "testuser@example.com"

    def test_user_does_not_exist(self):
        response = send_reset_password_email(self.user_email)

        self.assertEqual(400, response["status"])

    @patch("auth_service.email.render_to_string")
    @patch("auth_service.email.EmailMultiAlternatives")
    def test_email_sent_successfully(self, mock_email_class, mock_render_to_string):
        User.objects.create_user(
            email = "testuser@example.com", password = "test@123",
            first_name = "test_user", last_name = "test_user"
        )

        # Mock render_to_string
        mock_render_to_string.return_value = "<html>Reset your password</html>"

        # Mock EmailMultiAlternatives
        mock_email_instance = MagicMock()
        mock_email_class.return_value = mock_email_instance

        response = send_reset_password_email(self.user_email)

        self.assertEqual(response["status"], 200)
        mock_render_to_string.assert_called_once()
        mock_email_class.assert_called_once_with(
            subject="Reset your password",
            body="Reset your password",
            from_email="CartPe <%s>" % settings.EMAIL_HOST_USER,
            to=[self.user_email]
        )
        mock_email_instance.attach_alternative.assert_called_once_with("<html>Reset your password</html>", "text/html")
        mock_email_instance.send.assert_called_once()

    @patch("auth_service.email.render_to_string")
    @patch("auth_service.email.EmailMultiAlternatives")
    def test_exception_during_email_sending(self, mock_email_class, mock_render_to_string):
        User.objects.create_user(
            email = "testuser@example.com", password = "test@123",
            first_name = "test_user", last_name = "test_user"
        )

        # Mock render_to_string
        mock_render_to_string.return_value = "<html>Reset your password</html>"

        # Mock EmailMultiAlternatives to raise an exception
        mock_email_instance = MagicMock()
        mock_email_instance.send.side_effect = Exception("Email sending failed")
        mock_email_class.return_value = mock_email_instance

        response = send_reset_password_email(self.user_email)

        self.assertEqual(response["status"], 400)
        self.assertEqual(response["error"], "Email sending failed")
        mock_render_to_string.assert_called_once()
        mock_email_class.assert_called_once_with(
            subject="Reset your password",
            body="Reset your password",
            from_email="CartPe <%s>" % settings.EMAIL_HOST_USER,
            to=[self.user_email]
        )
        mock_email_instance.attach_alternative.assert_called_once_with("<html>Reset your password</html>", "text/html")
        mock_email_instance.send.assert_called_once()
