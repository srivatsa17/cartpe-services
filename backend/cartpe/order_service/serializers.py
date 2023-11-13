from rest_framework import serializers
from order_service.models import Order, OrderItem
from product_service.models import Product
from shipping_service.models import UserAddress
from shipping_service.serializers import UserAddressSerializer
import cartpe.settings as settings
import razorpay

RAZORPAY_CLIENT = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

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
    PENDING, CONFIRMED, SHIPPED = "PENDING", "CONFIRMED", "SHIPPED"
    OUT_FOR_DELIVERY, DELIVERED, CANCELLED =  "OUT_FOR_DELIVERY", "DELIVERED", "CANCELLED"

    ORDER_STATUS_CHOICES = [
        (PENDING, "Order Pending"),
        (CONFIRMED, "Order Confirmed"),
        (SHIPPED, "Shipped"),
        (OUT_FOR_DELIVERY, "Out for Delivery"),
        (DELIVERED, "Delivered"),
        (CANCELLED, "Cancelled")
    ]

    total_price = serializers.DecimalField(max_digits = 7, decimal_places = 2, coerce_to_string = False)
    user = serializers.SlugRelatedField(slug_field = 'email', read_only = True)
    user_address = serializers.SlugRelatedField(slug_field = 'id', queryset = UserAddress.objects.all())
    is_paid = serializers.BooleanField(default = False)
    status = serializers.ChoiceField(choices = ORDER_STATUS_CHOICES, default = PENDING)
    razorpay_order_id = serializers.CharField(min_length = 5, max_length = 50, read_only = True)
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only = True)

    class Meta:
        model = Order
        fields = [
            'id', 'total_price', 'user', 'user_address', 'is_paid', 'status', 'razorpay_order_id',
            'created_at', 'updated_at'
        ]

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        # Create order in RazorPay
        total_price = self.validated_data['total_price']

        razorpay_order = RAZORPAY_CLIENT.order.create({
            "amount": int(total_price) * 100,
            "currency": "INR",
            "payment_capture": "1"
        })

        validated_data['razorpay_order_id'] = razorpay_order['id']
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
