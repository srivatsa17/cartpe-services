from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from rest_framework.validators import UniqueTogetherValidator
from product_service.models import Product, Category, Brand, Image, Attribute, AttributeValue

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_empty_file = False)
    is_featured = serializers.BooleanField(default = None)
    product = serializers.PrimaryKeyRelatedField(read_only = True)
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only = True)

    class Meta:
        model = Image
        fields = ['id', 'image', 'is_featured', 'product', 'created_at', 'updated_at']

    def validate(self, attrs):
        is_featured = attrs.get('is_featured')
        productId = self.context.get('product')

        # productId will be None for Patch request since we wont send any query params for product.
        # in that case, we send imageId as a context from views to get the productId from Image model.
        if productId is None:
            productId = Image.objects.get(id = self.context.get('imageId')).product.id

        if is_featured and Image.objects.filter(product = productId, is_featured = True).exists():
            raise serializers.ValidationError({
                "message" : "is_featured=True cannot be set as there exists a featured image for productId " + str(productId)
            })

        return super().validate(attrs)

    def create(self, validated_data):
        productId = self.context.get('product')
        product = Product.objects.get(id = productId)
        validated_data['product'] = product
        return super().create(validated_data)

class AttributeValueSerializer(serializers.ModelSerializer):
    value = serializers.CharField(min_length = 1, max_length = 255, trim_whitespace = True)

    class Meta:
        model = AttributeValue
        fields = ['id', 'value']

class AttributeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length = 1, max_length = 255, trim_whitespace = True)
    attribute_values = AttributeValueSerializer(many = True, read_only = True)

    class Meta:
        model = Attribute
        fields = ['id', 'name', 'attribute_values']

class ProductSerializer(serializers.ModelSerializer):
    sku = serializers.UUIDField(format='hex_verbose', read_only = True)
    name = serializers.CharField(min_length = 1, max_length = 255, allow_blank = False, trim_whitespace = True)
    slug = serializers.SlugField(min_length = 1, max_length = 255, read_only = True)
    description = serializers.CharField(min_length = 1, max_length = 255, allow_blank = False, trim_whitespace = True)
    price = serializers.DecimalField(max_digits = 7, decimal_places = 2, coerce_to_string = False)
    brand = serializers.SlugRelatedField(slug_field = 'name', queryset = Brand.objects.all())
    stock_count = serializers.IntegerField(min_value = 0)
    discount = serializers.IntegerField(min_value = 0, max_value = 100)
    category = serializers.SlugRelatedField(slug_field = 'name', queryset = Category.objects.all())
    attributes = AttributeSerializer(many = True, read_only = True)
    product_images = ProductImageSerializer(many = True, read_only = True)
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only = True)

    class Meta:
        model = Product
        fields = [
            'id', 'sku', 'name', 'slug', 'description', 'price', 'brand', 'stock_count', 'discount', 'discounted_price',
            'selling_price', 'category', 'attributes', 'product_images', 'created_at', 'updated_at'
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
    level = serializers.IntegerField(read_only = True)
    parent = serializers.SlugRelatedField(slug_field = 'name', allow_null = True, queryset = Category.objects.all())
    children = RecursiveField(many = True, read_only = True)
    products = ProductSerializer(many = True, read_only = True)
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only = True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'level', 'parent', 'children', 'products', 'created_at', 'updated_at']
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

class BrandSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length = 1, max_length = 255, allow_blank = False, trim_whitespace = True)
    slug = serializers.SlugField(min_length = 1, max_length = 255, read_only = True)
    description = serializers.CharField(min_length = 1, max_length = 255, allow_blank = False, trim_whitespace = True)
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only = True)

    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'updated_at']

    def validate(self, attrs):
        brandName = attrs.get('name', '')
        isBrandFound = Brand.objects.filter(name__iexact = brandName).exists()

        if isBrandFound:
            raise serializers.ValidationError({
                "message" : "Brand '" + brandName + "' already exists and cannot be created or updated again."
            })

        return super().validate(attrs)

    def create(self, validated_data):
        brand = Brand.objects.create(**validated_data)
        return brand
