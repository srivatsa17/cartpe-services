from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from rest_framework.validators import UniqueTogetherValidator
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
        isProductFound = Product.objects.filter(name__iexact = productName).exists()

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
    parent = serializers.SlugRelatedField(slug_field = 'name', allow_null = True, queryset = Category.objects.all())
    children = RecursiveField(many = True, read_only = True)
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only = True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'children', 'created_at', 'updated_at']
        validators = [
            UniqueTogetherValidator(
                queryset = Category.objects.all(),
                fields = ['name', 'parent'],
            )
        ]

    def validate(self, attrs):
        categoryName = attrs.get('name', '')
        parentName = attrs.get('parent', '')
        
        isCategoryFound = Category.objects.filter(name__iexact = categoryName, parent = None).exists()

        # Handling special condition where parent can be Null.
        # This is not handled by UniqueTogetherValidator as there is no check for type 'None' in db by the validator.
        if parentName is None and isCategoryFound:
            raise serializers.ValidationError({
                "message" : "The fields name, parent must make a unique set."
            })

        return super().validate(attrs)

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category