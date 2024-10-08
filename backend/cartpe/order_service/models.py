from django.db import models
from auth_service.models import User
from shipping_service.models import UserAddress
from product_service.models import ProductVariant
from order_service.constants import OrderStatus, OrderMethod, OrderRefundStatus


# Create your models here.
class Order(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    amount_due = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    amount_refundable = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=False, blank=False, related_name="order"
    )
    user_address = models.ForeignKey(
        to=UserAddress, on_delete=models.PROTECT, null=False, blank=False, related_name="order"
    )
    is_paid = models.BooleanField(default=False, null=False, blank=False)
    status = models.CharField(
        max_length=255,
        choices=OrderStatus.ORDER_STATUS_CHOICES,
        default=OrderStatus.PENDING,
        null=False,
        blank=False,
    )
    refund_status = models.CharField(
        max_length=255,
        choices=OrderRefundStatus.ORDER_REFUND_STATUS_CHOICES,
        default=OrderRefundStatus.NA,
        null=False,
        blank=False,
    )
    method = models.CharField(
        max_length=255,
        choices=OrderMethod.ORDER_METHOD_CHOICES,
        default=OrderMethod.UPI,
        null=False,
        blank=False,
    )
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=255, null=True, blank=True)
    razorpay_refund_id = models.CharField(max_length=255, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class OrderItem(models.Model):
    order = models.ForeignKey(
        to=Order, on_delete=models.CASCADE, null=False, blank=False, related_name="order_item"
    )
    product_variant = models.ForeignKey(
        to=ProductVariant,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="order_item",
    )
    quantity = models.PositiveSmallIntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.pk)
