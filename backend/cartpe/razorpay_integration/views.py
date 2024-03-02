from .import RAZORPAY_CLIENT
from rest_framework.serializers import ValidationError

class RazorPayAPIView():
    """
    Class designed to handle interactions with the RazorPay API using the razorpay client.
    """
    def create_order(self, **kwargs):
        data = {
            "amount": int(kwargs['amount']) * 100,
            "currency": "INR",
            "payment_capture": "1"
        }

        try:
            order_details = RAZORPAY_CLIENT.order.create(data = data)
            return order_details

        except Exception:
            raise ValidationError("Failed to create razorpay order.")
        
    def fetch_order(self, **kwargs):
        order_id = kwargs['razorpay_order_id']

        try:
            order_details = RAZORPAY_CLIENT.order.fetch(order_id)
            return order_details

        except Exception:
            raise ValidationError(f"Failed to fetch razorpay order {order_id}.")

    def verify_payment_signature(self, **kwargs):
        try:
            verify_signature = RAZORPAY_CLIENT.utility.verify_payment_signature({
                'razorpay_order_id': kwargs['razorpay_order_id'],
                'razorpay_payment_id': kwargs['razorpay_payment_id'],
                'razorpay_signature': kwargs['razorpay_signature']
            })
            return verify_signature

        except Exception:
            raise ValidationError("Failed to verify the payment signature.")

razorpay_api_client = RazorPayAPIView()