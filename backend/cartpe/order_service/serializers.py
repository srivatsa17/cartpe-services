from rest_framework import serializers
from order_service.models import Order, OrderItem
from product_service.models import Product
from shipping_service.models import UserAddress
from order_service.constants import OrderStatus, OrderMethod

class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.SlugRelatedField(slug_field = 'id', read_only = True)
    product = serializers.SlugRelatedField(slug_field = 'id', queryset = Product.objects.all())
    quantity = serializers.IntegerField(min_value = 1, max_value = 10)
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only = True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'created_at', 'updated_at']

class OrderSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits = 7, decimal_places = 2, coerce_to_string = False)
    user = serializers.SlugRelatedField(slug_field = 'email', read_only = True)
    user_address = serializers.SlugRelatedField(slug_field = 'id', queryset = UserAddress.objects.all())
    is_paid = serializers.BooleanField(default = False)
    status = serializers.ChoiceField(choices = OrderStatus.ORDER_STATUS_CHOICES, default = OrderStatus.PENDING)
    method = serializers.ChoiceField(choices = OrderMethod.ORDER_METHOD_CHOICES, default = OrderMethod.UPI)
    razorpay_order_id = serializers.CharField(min_length = 1, max_length = 50, allow_null = True, allow_blank = True)
    razorpay_payment_id = serializers.CharField(min_length = 1, max_length = 50, allow_null = True, allow_blank = True)
    razorpay_signature = serializers.CharField(min_length = 1, max_length = 255, allow_null = True, allow_blank = True)
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only = True)

    class Meta:
        model = Order
        fields = [
            'id', 'amount', 'user', 'user_address', 'is_paid', 'status', 'method', 'razorpay_order_id', 
            'razorpay_payment_id', 'razorpay_signature', 'created_at', 'updated_at'
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
        # Serialize order_items
        order_items_data = OrderItemSerializer(order_items_queryset, many = True).data
        # Include order_items in the representation
        representation['order_items'] = order_items_data
        return representation
