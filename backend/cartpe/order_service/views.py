from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from order_service.models import Order, OrderItem
from order_service.serializers import OrderSerializer, OrderItemSerializer
from order_service.constants import OrderStatus, OrderMethod
from razorpay_integration.views import razorpay_api_client
from razorpay_integration.serializers import RazorPayOrderSerializer
from payment_service.models import Payment
from payment_service.serializers import PaymentSerializer

# Create your views here.

class RazorPayOrderAPIView(generics.GenericAPIView):
    """
    RazorPayOrderAPIView is designed to create an order in razorpay using razorpay client library.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RazorPayOrderSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if  serializer.is_valid():
            razorpay_order = razorpay_api_client.create_order(
                amount = serializer.validated_data.get("amount")
            )

            return Response(razorpay_order, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class OrderAPIView(generics.GenericAPIView):
    """
    OrderAPIView will check for payment status using razorpay client library.
    If payment is successful, it creates order and order items in their respective models.
    If payment failed, order and order items are not created.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        orders = (
                    Order.objects
                    .select_related('user', 'user_address')
                    .filter(user = self.get_object())
                    .order_by('-created_at')
                )
        return orders

    def get(self, request):
        orders = self.get_queryset()
        serializer = self.serializer_class(orders, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        order_items_serializer = OrderItemSerializer(data = request.data.get('order_items'), many = True)
        payment_serializer = PaymentSerializer(data = request.data.get('payment_details'))

        if  serializer.is_valid() and order_items_serializer.is_valid() and payment_serializer.is_valid():
            if serializer.validated_data['method'] == OrderMethod.UPI:
                razorpay_api_client.verify_payment_signature(
                    razorpay_order_id = serializer.validated_data.get("razorpay_order_id"),
                    razorpay_payment_id = serializer.validated_data.get("razorpay_payment_id"),
                    razorpay_signature = serializer.validated_data.get("razorpay_signature")
                )
                serializer.validated_data['is_paid'] = True
            else:
                serializer.validated_data['is_paid'] = False

            serializer.validated_data['user'] = self.get_object()
            serializer.validated_data['status'] = OrderStatus.CONFIRMED
            
            order = serializer.save()

            # We are creating a list of OrderItem objects because of bulk_create method on OrderItem class.
            order_items = [
                OrderItem(order=order, **order_item) for order_item in order_items_serializer.validated_data
            ]

            OrderItem.objects.bulk_create(order_items)

            # Create the payment
            Payment.objects.create(order = order, **payment_serializer.validated_data)

            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(
            serializer.errors or payment_serializer.errors or order_items_serializer.errors, 
            status = status.HTTP_400_BAD_REQUEST
        )