from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import redis

# Initialise JSON redis instance
redis_client = redis.Redis().json()

class CartSerializer(serializers.Serializer):
    product = serializers.DictField()
    quantity = serializers.IntegerField(min_value=1, max_value=10)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        # Setting product_id as 0 incase product obj is empty to prevent 500 response.
        product_id = attrs.get('product')['id'] if attrs.get('product') else 0
        redis_key = self.context.get('redis_key', '')
        empty_cart = { "cartItems": [] }
        cart_items_path_in_redis = '$.cartItems'
        index = -1
        cart_item_obj = None

        try:
            if redis_client.get(redis_key) is None:
                redis_client.set(redis_key, '$', empty_cart)

            cart_items = redis_client.get(redis_key, cart_items_path_in_redis)[0]
            for cart_item in cart_items:
                index += 1
                if cart_item['product']['id'] == product_id:
                    cart_item_obj = cart_item
                    break

            if cart_item_obj:
                raise ValidationError("Product already exists in cart.")

            return attrs

        except redis.ConnectionError:
            raise ValidationError("Redis server is down.")

        except redis.TimeoutError:
            raise ValidationError("Redis server is slow or unable to respond.")

class CartByIdSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, max_value=10, required=False)

    class Meta:
        fields = ['quantity']

    def get_fields(self):
        fields = super().get_fields()
        if self.context.get('request_method') == 'PATCH':
            fields['quantity'].required = True
        return fields

    def validate(self, attrs):
        quantity = attrs.get('quantity', 1)
        redis_key = self.context.get('redis_key', '')
        product_id = self.context.get('product_id', '')
        cart_items_path_in_redis = '$.cartItems'
        index = -1
        cart_item_obj = None

        try:
            if redis_client.get(redis_key) is None:
                raise ValidationError("Empty cart found for user.")

            if redis_client.get(redis_key, cart_items_path_in_redis) is None:
                raise ValidationError("CartItems not found.")

            cart_items = redis_client.get(redis_key, cart_items_path_in_redis)[0]
            for cart_item in cart_items:
                index += 1
                if cart_item['product']['id'] == product_id:
                    cart_item_obj = cart_item
                    break

            if cart_item_obj is None:
                raise ValidationError("Requested cart item is not found.")

            if index == -1 or index == redis_client.arrlen(redis_key, cart_items_path_in_redis):
                raise ValidationError("Requested cart item is not found.")

            if self.context.get('request_method') == 'PATCH' and cart_item_obj['quantity'] == quantity:
                raise ValidationError("New quantity provided is same as previous quantity.")

            return {
                "index": index,
                "quantity": quantity
            }

        except redis.ConnectionError:
            raise ValidationError("Redis server is down.")

        except redis.TimeoutError:
            raise ValidationError("Redis server is slow or unable to respond.")