from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from cart_service.routes import routes
from cart_service.serializers import CartSerializer, CartByIdSerializer
from django.core.cache import cache

class RoutesAPIView(generics.GenericAPIView):
    queryset = routes

    def get(self, request):
        return Response(self.get_queryset())

class CartAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_redis_cache_key(self):
        return "user:{user}:cart".format(user = self.request.user)

    def get_default_response(self):
        default_response = { "cartItems": [] }
        return default_response

    """
    Get the list of cartItems for a user
    """
    def get(self, request):
        response = cache.get(key=self.get_redis_cache_key(), default=self.get_default_response())
        return Response(response, status = status.HTTP_200_OK)

    """
    Add the new cartItem at the tail of the list of cartItems
    """
    def post(self, request):
        cart = cache.get(self.get_redis_cache_key(), default=self.get_default_response())

        context = { "cart": cart }
        serializer = self.serializer_class(data = request.data, context = context)

        if serializer.is_valid():
            cart["cartItems"].append(serializer.validated_data)

            cache.set(key=self.get_redis_cache_key(), value=cart, timeout=None)

            return Response(cart, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Empty the cart by deleting the redis_key
    """
    def delete(self, request):
        cache.delete(self.get_redis_cache_key())
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartByIdAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartByIdSerializer

    def get_redis_cache_key(self):
        return "user:{user}:cart".format(user = self.request.user)

    def get_default_response(self):
        default_response = { "cartItems": [] }
        return default_response

    """
    Update the quantity of a particular cartItem in the list of cartItems
    """
    def patch(self, request, id):
        cart = cache.get(self.get_redis_cache_key(), default=self.get_default_response())

        context = { "cart": cart, "product_id": id }
        serializer = self.serializer_class(data = request.data, context = context)

        if serializer.is_valid():
            [
                cart_item.update({ "quantity": serializer.validated_data["quantity"] }) \
                for cart_item in cart["cartItems"] if cart_item["product"]["id"] == id
            ]

            cache.set(key=self.get_redis_cache_key(), value=cart, timeout=None)

            return Response(cart, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Remove the cartItem from the list of cartItems
    """
    def delete(self, request, id):
        cart = cache.get(self.get_redis_cache_key(), default=self.get_default_response())

        context = { "cart": cart, "product_id": id }
        serializer = self.serializer_class(data = request.data, context = context)

        if serializer.is_valid():
            new_cart_items = [cart_item for cart_item in cart["cartItems"] if cart_item["product"]["id"] != id]
            cart["cartItems"] = new_cart_items

            cache.set(key=self.get_redis_cache_key(), value=cart, timeout=None)

            return Response(cart, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
