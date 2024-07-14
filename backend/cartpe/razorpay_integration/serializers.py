from rest_framework import serializers


class RazorPayOrderSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=7, decimal_places=2, coerce_to_string=False)
