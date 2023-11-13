from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from order_service.models import Order, OrderItem
from order_service.serializers import OrderSerializer, OrderItemSerializer

# Create your views here.

class OrderAPIView(generics.GenericAPIView):
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

        if serializer.is_valid() and order_items_serializer.is_valid():
            serializer.validated_data['user'] = self.get_object()
            order = serializer.save()

            # We are creating a list of OrderItem objects because of bulk_create method on OrderItem class.
            order_items = [
                OrderItem(order=order, **order_item) for order_item in order_items_serializer.validated_data
            ]

            OrderItem.objects.bulk_create(order_items)

            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)