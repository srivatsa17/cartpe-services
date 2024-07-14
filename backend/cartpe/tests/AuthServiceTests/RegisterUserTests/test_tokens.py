from django.test import TestCase
import six
from datetime import datetime
from auth_service.models import User
from auth_service.token import AccountActivationTokenGenerator


class AccountActivationTokenGeneratorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="testuser@example.com", password="testuser")
        self.token_generator = AccountActivationTokenGenerator()

    def test_make_hash_value(self):
        timestamp = datetime.now()
        expected_hash = (
            six.text_type(self.user.pk)
            + six.text_type(timestamp)
            + six.text_type(self.user.is_verified)
        )
        generated_hash = self.token_generator._make_hash_value(self.user, timestamp)
        self.assertEqual(generated_hash, expected_hash)

    def test_token_generation(self):
        token = self.token_generator.make_token(self.user)
        self.assertNotEqual(token, "")

        is_valid = self.token_generator.check_token(self.user, token)
        self.assertTrue(is_valid)

        self.user.is_verified = True
        self.user.save()

        is_valid = self.token_generator.check_token(self.user, token)
        self.assertFalse(is_valid)
