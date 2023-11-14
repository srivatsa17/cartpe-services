from django.db import models
from auth_service.models import User
from shipping_service.models import UserAddress
from product_service.models import Product

# Create your models here.
class Order(models.Model):
    PENDING, CONFIRMED, SHIPPED, OUT_FOR_DELIVERY = "PENDING", "CONFIRMED", "SHIPPED", "OUT_FOR_DELIVERY"
    DELIVERED, CANCELLED, RETURNED = "DELIVERED", "CANCELLED", "RETURNED"

    ORDER_STATUS_CHOICES = [
        (PENDING, "Order Pending"),
        (CONFIRMED, "Order Confirmed"),
        (SHIPPED, "Shipped"),
        (OUT_FOR_DELIVERY, "Out for Delivery"),
        (DELIVERED, "Delivered"),
        (CANCELLED, "Cancelled"),
        (RETURNED, "Returned")
    ]

    amount = models.DecimalField(max_digits = 7, decimal_places = 2, null = False, blank = False)
    user = models.ForeignKey(to = User, on_delete = models.CASCADE, null = False, blank = False, related_name = 'order')
    user_address = models.ForeignKey(to = UserAddress, on_delete = models.CASCADE, null = False, blank = False, related_name = 'order')
    is_paid = models.BooleanField(default = False, null = False, blank = False)
    status = models.CharField(max_length = 255, choices = ORDER_STATUS_CHOICES, default = PENDING, null = False, blank = False)
    razorpay_order_id = models.CharField(max_length = 255, null = False, blank = False)
    razorpay_payment_id = models.CharField(max_length = 255, null = False, blank = False)
    razorpay_signature = models.CharField(max_length = 255, null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return self.pk

class OrderItem(models.Model):
    order = models.ForeignKey(to = Order, on_delete = models.CASCADE, null = False, blank = False, related_name = 'order_item')
    product = models.ForeignKey(to = Product, on_delete = models.PROTECT, null = False, blank = False, related_name = 'order_item')
    quantity = models.PositiveSmallIntegerField(null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return self.order.razorpay_order_id