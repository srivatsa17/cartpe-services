from rest_framework import serializers
from payment_service.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.SlugRelatedField(slug_field="id", read_only=True)
    total_mrp = serializers.DecimalField(max_digits=7, decimal_places=2, coerce_to_string=False)
    total_discount_price = serializers.DecimalField(
        max_digits=7, decimal_places=2, coerce_to_string=False
    )
    total_selling_price = serializers.DecimalField(
        max_digits=7, decimal_places=2, coerce_to_string=False
    )
    convenience_fee = serializers.IntegerField()
    shipping_fee = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=7, decimal_places=2, coerce_to_string=False)
    round_off_price = serializers.DecimalField(
        max_digits=7, decimal_places=2, coerce_to_string=False
    )
    savings_amount = serializers.DecimalField(
        max_digits=7, decimal_places=2, coerce_to_string=False
    )
    savings_percent = serializers.DecimalField(
        max_digits=7, decimal_places=2, coerce_to_string=False
    )
    created_at = serializers.DateTimeField(read_only=True, format="%d %b %Y, %H:%M")
    updated_at = serializers.DateTimeField(read_only=True, format="%d %b %Y, %H:%M")

    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "total_mrp",
            "total_discount_price",
            "total_selling_price",
            "convenience_fee",
            "shipping_fee",
            "total_amount",
            "round_off_price",
            "savings_amount",
            "savings_percent",
            "created_at",
            "updated_at",
        ]
