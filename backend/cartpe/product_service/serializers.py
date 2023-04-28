from rest_framework import serializers
from .models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    sku = serializers.UUIDField(format='hex_verbose', read_only = True)
    name = serializers.CharField(min_length = 1, max_length = 255, allow_blank = False, trim_whitespace = True)
    slug = serializers.SlugField(min_length = 1, max_length = 255, read_only = True)
    description = serializers.CharField(min_length = 1, max_length = 255, allow_blank = False, trim_whitespace = True)
    price = serializers.DecimalField(max_digits = 7, decimal_places = 2, coerce_to_string = False)
    brand = serializers.CharField(min_length = 1, max_length = 255, allow_blank = False, trim_whitespace = True)
    stock_count = serializers.IntegerField(min_value = 0)
    discount = serializers.IntegerField(min_value = 0, max_value = 100)
    category = serializers.SlugRelatedField(slug_field = 'name', queryset = Category.objects.all())
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only = True)

    class Meta:
        model = Product
        fields = [
            'id', 'sku', 'name', 'slug', 'description', 'price', 'brand', 'stock_count', 'discount', 'discounted_price', 'selling_price', 'category', 'created_at',
            'updated_at'
        ]

    def validate(self, attrs):
        productName = attrs.get('name', '')
        isProductFound = Product.objects.filter(name = productName).exists()

        if isProductFound:
            raise serializers.ValidationError({
                "message" : "Product '" + productName + "' already exists and cannot be created or updated again."
            })

        return super().validate(attrs)

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length = 1, max_length = 255, allow_blank = False, trim_whitespace = True)
    slug = serializers.SlugField(min_length = 1, max_length = 255, read_only = True)
    description = serializers.CharField(min_length = 1, max_length = 255, allow_blank = False, trim_whitespace = True)
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only = True)

    class Meta:
        model = Category
        fields = '__all__'

    def validate(self, attrs):
        categoryName = attrs.get('name', '')
        isCategoryFound = Category.objects.filter(name = categoryName).exists()

        if isCategoryFound:
            raise serializers.ValidationError({
                "message" : "Category '" + categoryName + "' already exists and cannot be created or updated again."
            })

        return super().validate(attrs)

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category