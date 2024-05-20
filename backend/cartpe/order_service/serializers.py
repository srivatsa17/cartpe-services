from rest_framework import serializers
from order_service.models import Order, OrderItem
from order_service.constants import OrderStatus, OrderMethod, OrderRefundStatus
from product_service.models import Product, ProductVariant
from product_service.serializers import ProductVariantSerializer
from shipping_service.models import UserAddress
from shipping_service.serializers import UserAddressSerializer
from payment_service.models import Payment
from payment_service.serializers import PaymentSerializer

class OrderItemProductSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="brand.name", read_only = True)
    category = serializers.CharField(source="category.name", read_only = True)
    category_slug = serializers.CharField(source="category.slug", read_only = True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "description", "brand", "category", "category_slug"]

class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.SlugRelatedField(slug_field = 'id', read_only = True)
    product = OrderItemProductSerializer(source="product_variant.product", read_only=True)
    product_variant = serializers.SlugRelatedField(slug_field = 'id', queryset = ProductVariant.objects.all())
    quantity = serializers.IntegerField(min_value = 1, max_value = 10)
    created_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")
    updated_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_variant', 'quantity', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["product_variant"] = ProductVariantSerializer(instance=instance.product_variant).data
        return representation

class OrderSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits = 7, decimal_places = 2, coerce_to_string = False)
    amount_paid = serializers.DecimalField(max_digits = 7, decimal_places = 2, coerce_to_string = False, read_only = True)
    amount_due = serializers.DecimalField(max_digits = 7, decimal_places = 2, coerce_to_string = False, read_only = True)
    amount_refundable = serializers.DecimalField(default = 0, max_digits = 7, decimal_places = 2, coerce_to_string = False)
    user = serializers.SlugRelatedField(slug_field = 'email', read_only = True)
    user_address = serializers.SlugRelatedField(slug_field = 'id', queryset = UserAddress.objects.all())
    is_paid = serializers.BooleanField(default = False)
    status = serializers.ChoiceField(choices = OrderStatus.ORDER_STATUS_CHOICES, default = OrderStatus.PENDING)
    refund_status = serializers.ChoiceField(choices = OrderRefundStatus.ORDER_REFUND_STATUS_CHOICES, default = OrderRefundStatus.NA)
    method = serializers.ChoiceField(choices = OrderMethod.ORDER_METHOD_CHOICES, default = OrderMethod.UPI)
    razorpay_order_id = serializers.CharField(min_length = 1, max_length = 50, allow_null = True, allow_blank = True)
    razorpay_payment_id = serializers.CharField(min_length = 1, max_length = 50, allow_null = True, allow_blank = True)
    razorpay_signature = serializers.CharField(min_length = 1, max_length = 255, allow_null = True, allow_blank = True)
    created_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")
    updated_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")

    class Meta:
        model = Order
        fields = [
            'id', 'amount', 'amount_paid', 'amount_due', 'amount_refundable', 'user', 'user_address', 'is_paid', 
            'status', 'method', 'refund_status', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 
            'razorpay_refund_id', 'created_at', 'updated_at'
        ]

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    # Modifying the serialized response to include order_items pertaining to the order instance.
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Retrieve order_items related to the current Order instance
        order_items_queryset = OrderItem.objects.filter(order = instance).order_by("-created_at")
        # Include order_items in the representation
        representation['order_items'] = OrderItemSerializer(order_items_queryset, many = True).data
        representation['user_address'] = UserAddressSerializer(instance.user_address).data

        # Retrieve payment related to the current Order instance and include it in representation
        payment_queryset = Payment.objects.get(order = instance)
        representation['payment_details'] = PaymentSerializer(payment_queryset).data

        return representation
