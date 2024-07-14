from django.db import models
from auth_service.models import User
from customer_service.constants import CustomerService


class ContactUs(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=False, blank=False, related_name="contact_us"
    )
    topic = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        choices=CustomerService.TOPIC_CHOICES,
        default=CustomerService.ORDER_STATUS,
    )
    comment = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.topic
