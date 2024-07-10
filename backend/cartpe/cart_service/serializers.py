from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class CartSerializer(serializers.Serializer):
    product = serializers.DictField()
    quantity = serializers.IntegerField(min_value=1, max_value=10)

    def validate(self, attrs):
        product = attrs.get("product")
        cart = self.context.get("cart")

        if any(cart_item["product"]["id"] == product["id"] for cart_item in cart["cartItems"]):
            raise ValidationError("Product already exists in cart.")

        return attrs

class CartByIdSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, max_value=10, required=False)

    class Meta:
        fields = ['quantity']

    def validate(self, attrs):
        cart = self.context.get("cart")
        product_id = self.context.get("product_id")

        if not cart or not cart["cartItems"]:
            raise ValidationError("Cart is empty")

        if not any(cart_item["product"]["id"] == product_id for cart_item in cart["cartItems"]):
            raise ValidationError(f"Product with id = {product_id} does not exist in the cart.")

        return attrs
