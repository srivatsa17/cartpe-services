from unittest.mock import patch
from django.test import TestCase
from rest_framework.serializers import ValidationError
from razorpay_integration.views import RazorPayAPIView

class TestRazorPayAPIView(TestCase):
    @patch("razorpay_integration.views.RAZORPAY_CLIENT.order.create")
    def test_create_order_success(self, mock_order_create):
        razorpay_api = RazorPayAPIView()
        mock_order_create.return_value = { "id": "mock_order_id", "amount": 100, "currency": "INR" }

        order_details = razorpay_api.create_order(amount = 1)

        self.assertEqual(order_details["id"], "mock_order_id")
        self.assertEqual(order_details["amount"], 100)
        self.assertEqual(order_details["currency"], "INR")

    @patch("razorpay_integration.views.RAZORPAY_CLIENT.order.create")
    def test_create_order_failure(self, mock_order_create):
        razorpay_api = RazorPayAPIView()
        mock_order_create.side_effect = Exception("Failed to create razorpay order.")

        # Call the create_order method and expect a ValidationError
        with self.assertRaises(ValidationError) as response:
            razorpay_api.create_order(amount = 1)

        self.assertEqual(str(response.exception.detail[0]), "Failed to create razorpay order.")

    @patch("razorpay_integration.views.RAZORPAY_CLIENT.utility.verify_payment_signature")
    def test_verify_payment_signature_success(self, mock_verify_signature):
        razorpay_api = RazorPayAPIView()
        mock_verify_signature.return_value = { "razorpay_signature": "verified_signature" }

        # Call the verify_payment_signature method
        signature_result = razorpay_api.verify_payment_signature(
            razorpay_order_id = "mock_order_id",
            razorpay_payment_id = "mock_payment_id",
            razorpay_signature = "verified_signature"
        )

        self.assertEqual(signature_result["razorpay_signature"], "verified_signature")

    @patch("razorpay_integration.views.RAZORPAY_CLIENT.utility.verify_payment_signature")
    def test_verify_payment_signature_failure(self, mock_verify_signature):
        razorpay_api = RazorPayAPIView()
        mock_verify_signature.side_effect = Exception

        # Call the verify_payment_signature method and expect a ValidationError
        with self.assertRaises(ValidationError) as response:
            razorpay_api.verify_payment_signature(
                razorpay_order_id = "mock_order_id",
                razorpay_payment_id = "mock_payment_id",
                razorpay_signature = "invalid_signature"
            )

        self.assertEqual(str(response.exception.detail[0]), "Failed to verify the payment signature.")
