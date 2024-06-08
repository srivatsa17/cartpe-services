from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from cart_service.routes import routes
from cart_service.serializers import CartSerializer, CartByIdSerializer
import redis

# Initialise JSON redis instance
redis_client = redis.Redis().json()

class RoutesAPIView(generics.GenericAPIView):
    queryset = routes

    def get(self, request):
        return Response(self.get_queryset())

class CartAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        return self.request.user.id

    def get_redis_key(self):
        user_id = self.get_object()
        return "cart:%s" % user_id

    def get_serializer_context(self):
        return {
            "redis_key": self.get_redis_key()
        }

    def get_cart_list(self, redis_key):
        cart_items = redis_client.get(redis_key)
        if cart_items is None:
            # Setting an empty cart if redis response is null.
            return { "cartItems": [] }
        return cart_items

    """
    Get the list of cartItems for a user
    """
    def get(self, request):
        redis_key = self.get_redis_key()
        response = self.get_cart_list(redis_key)
        return Response(response, status = status.HTTP_200_OK)

    """
    Add the new cartItem at the tail of the list of cartItems
    """
    def post(self, request):
        redis_key = self.get_redis_key()
        context = self.get_serializer_context()
        serializer = self.serializer_class(data = request.data, context = context)

        if serializer.is_valid():
            redis_client.arrappend(redis_key, '$.cartItems', serializer.validated_data)
            response = self.get_cart_list(redis_key)
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Empty the cart by deleting the redis_key
    """
    def delete(self, request):
        redis_key = self.get_redis_key()
        redis_client.delete(redis_key)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartByIdAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartByIdSerializer

    def get_object(self):
        return self.request.user.id

    def get_redis_key(self):
        user_id = self.get_object()
        return "cart:%s" % user_id

    def get_serializer_context(self, redis_key, product_id, request_method):
        return {
            "request_method": request_method,
            "redis_key": redis_key,
            "product_id": product_id
        }

    def get_cart_list(self, redis_key):
        cart_items = redis_client.get(redis_key)
        if cart_items is None:
            # Setting an empty cart if redis response is null.
            return { "cartItems": [] }
        return cart_items

    """
    Update the quantity of a particular cartItem in the list of cartItems
    """
    def patch(self, request, id):
        redis_key = self.get_redis_key()
        context = self.get_serializer_context(redis_key, id, request.method)
        serializer = self.serializer_class(data = request.data, context = context)

        if serializer.is_valid():
            index = serializer.validated_data['index']
            quantity = serializer.validated_data['quantity']
            redis_client.execute_command('JSON.SET', redis_key, '$.cartItems[%d].quantity' % index, quantity)
            return Response(self.get_cart_list(redis_key), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Remove the cartItem from the list of cartItems
    """
    def delete(self, request, id):
        redis_key = self.get_redis_key()
        context = self.get_serializer_context(redis_key, id, request.method)
        serializer = self.serializer_class(data = request.data, context = context)

        if serializer.is_valid():
            index = serializer.validated_data['index']
            redis_client.delete(redis_key, '$.cartItems[%d]' % index)
            return Response(self.get_cart_list(redis_key), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)