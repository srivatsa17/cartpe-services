import razorpay
import cartpe.settings as settings

# Initialize the RazorPay client by passing the razorpay key id and secret obtained from key generation in razorpay dashboard.
# Razorpay dashboard link: https://dashboard.razorpay.com/app/dashboard

RAZORPAY_CLIENT = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
