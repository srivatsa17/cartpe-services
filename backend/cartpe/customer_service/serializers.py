from rest_framework import serializers
from auth_service.models import User
from customer_service.models import ContactUs
from customer_service.constants import CustomerService

class ContactUsSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field = "email", read_only = True)
    topic = serializers.ChoiceField(choices = CustomerService.TOPIC_CHOICES)
    comment = serializers.CharField()
    created_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")
    updated_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")

    class Meta:
        model = ContactUs
        fields = [ "id", "user", "topic", "comment", "created_at", "updated_at" ]
