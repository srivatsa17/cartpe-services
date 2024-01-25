from rest_framework import serializers
from order_service.models import Order, OrderItem
from order_service.constants import OrderStatus, OrderMethod
from product_service.models import Product, Image
from shipping_service.models import UserAddress
from shipping_service.serializers import UserAddressSerializer
from payment_service.models import Payment
from payment_service.serializers import PaymentSerializer

class OrderItemProductSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()
    featured_image = serializers.SerializerMethodField()

    def get_brand(self, obj):
        return obj.brand.name

    def get_featured_image(self, obj):
        # Retrieve the featured image for the product
        return Image.objects.filter(product=obj, is_featured=True).first().image

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'brand', 'featured_image']

class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.SlugRelatedField(slug_field = 'id', read_only = True)
    product = serializers.SlugRelatedField(slug_field = 'id', queryset = Product.objects.all())
    quantity = serializers.IntegerField(min_value = 1, max_value = 10)
    created_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")
    updated_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["product"] = OrderItemProductSerializer(instance=instance.product).data
        return representation

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
    created_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")
    updated_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")

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
        # Include order_items in the representation
        representation['order_items'] = OrderItemSerializer(order_items_queryset, many = True).data
        representation['user_address'] = UserAddressSerializer(instance.user_address).data

        # Retrieve payment related to the current Order instance and include it in representation
        payment_queryset = Payment.objects.get(order = instance)
        representation['payment_details'] = PaymentSerializer(payment_queryset).data

        return representation
