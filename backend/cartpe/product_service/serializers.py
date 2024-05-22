from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from rest_framework.validators import UniqueTogetherValidator
from product_service.models import (
    ProductVariantPropertyValue, ProductVariantProperty, ProductVariant, Product, Category, Brand, WishList,
    ProductReview
)
from django.db.models import Avg, Count

class ProductReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the `ProductReview` model's fields.
    """
    product = serializers.SlugRelatedField(slug_field="id", queryset=Product.objects.all())
    user = serializers.SerializerMethodField(read_only=True)
    headline = serializers.CharField(min_length=1, max_length=255)
    rating = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField(min_length=1, max_length=500, required=False, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True, format="%d %b %Y, %H:%M")
    updated_at = serializers.DateTimeField(read_only=True, format="%d %b %Y, %H:%M")

    def get_user(self, instance):
        return f"{instance.user.first_name} {instance.user.last_name}"

    class Meta:
        model = ProductReview
        fields = ["id", "product", "user", "headline", "rating", "comment", "created_at", "updated_at"]

class ProductVariantPropertyValueSerializer(serializers.ModelSerializer):
    """
    Serializer for the `ProductVariantPropertyValue` model's fields.
    """
    name = serializers.CharField(source="property.name", min_length=1, max_length=255)
    value = serializers.CharField(min_length=1, max_length=255)

    class Meta:
        model = ProductVariantPropertyValue
        fields = ["id", "property_id", "name", "value"]

class ProductVariantSerializer(serializers.ModelSerializer):
    """
    Serializer for the `ProductVariant` model's fields.
    """
    name = serializers.CharField(min_length=1, max_length=255, read_only=True)
    sku = serializers.UUIDField(format="hex_verbose", read_only=True)
    images = serializers.ListField(child=serializers.URLField(max_length=255))
    price = serializers.DecimalField(max_digits=7, decimal_places=2, coerce_to_string=False)
    discount = serializers.IntegerField(min_value=0, max_value=100)
    stock_count = serializers.IntegerField(min_value=0)
    properties = ProductVariantPropertyValueSerializer(many=True)
    available_properties = serializers.SerializerMethodField(read_only = True)
    created_at = serializers.DateTimeField(read_only=True, format="%d %b %Y, %H:%M")
    updated_at = serializers.DateTimeField(read_only=True, format="%d %b %Y, %H:%M")

    def get_available_properties(self, instance):
        return list({p.property.name for p in instance.properties.all()})

    class Meta:
        model = ProductVariant
        fields = [
            "id", "product_id", "name", "sku", "images", "price", "discount", "discounted_price", "selling_price",
            "stock_count", "properties", "available_properties", "created_at", "updated_at",
        ]

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Product` model's fields.
    """
    name = serializers.CharField(min_length=1, max_length=255)
    slug = serializers.SlugField(min_length=1, max_length=255, read_only=True)
    description = serializers.CharField(min_length=1, max_length=255)
    brand = serializers.SlugRelatedField(slug_field="name", queryset=Brand.objects.all())
    category = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all())
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    product_variants = ProductVariantSerializer(many=True)
    product_reviews = ProductReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField(read_only=True)
    review_count = serializers.SerializerMethodField(read_only=True)
    rating_counts = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%d %b %Y, %H:%M")
    updated_at = serializers.DateTimeField(read_only=True, format="%d %b %Y, %H:%M")

    def get_average_rating(self, obj):
        average_rating = ProductReview.objects.filter(product=obj).aggregate(Avg('rating'))['rating__avg']
        return average_rating if average_rating is not None else 0
    
    def get_review_count(self, obj):
        review_count = ProductReview.objects.filter(product=obj).count()
        return review_count
    
    def get_rating_counts(self, obj):
        rating_counts = (
            ProductReview.objects
            .filter(product=obj)
            .values('rating')
            .annotate(count=Count('rating'))
            .order_by('rating')
        )

        # Create a dictionary to hold the counts for each rating value from 1 to 5
        rating_dict = {i: 0 for i in range(1, 6)}
        for rating in rating_counts:
            rating_dict[rating['rating']] = rating['count']
        return rating_dict

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "brand", "category", "category_slug",
            "product_variants", "product_reviews", "average_rating", "review_count", 
            "rating_counts", "created_at", "updated_at",
        ]

    def validate(self, attrs):
        productName = attrs.get("name", "")

        if Product.objects.filter(name__iexact=productName).exists():
            raise serializers.ValidationError({
                "message": "Product '" + productName + "' already exists and cannot be created again."
            })

        return super().validate(attrs)

    def create(self, validated_data):
        """
        Method to create a new product instance using validated data.

        This method extracts product variant data from the validated data,
        creates a new Product instance, and associates it with the product variants.
        It also creates associated variant properties and values as necessary.

        Returns a `Product` instance.
        """
        product_variants = validated_data.pop("product_variants")
        product = Product.objects.create(**validated_data)

        for product_variant in product_variants:
            properties = product_variant.pop("properties", [])

            # Join all property values by "-", append it to the product name and assign this value to product variant name.
            property_values = "-".join(property_data["value"] for property_data in properties)
            if property_values:
                product_variant_name = product.name + " - " + property_values
            else:
                product_variant_name = product.name

            product_variant_instance = ProductVariant.objects.create(
                name=product_variant_name, product=product, **product_variant
            )

            for property_data in properties:
                property_name = property_data["property"]["name"]
                property_value = property_data["value"]

                property_instance, _ = ProductVariantProperty.objects.get_or_create(name__iexact=property_name)
                property_value_instance, _ = (
                    ProductVariantPropertyValue.objects.get_or_create(property=property_instance, value=property_value)
                )

                product_variant_instance.properties.add(property_value_instance)

        return product

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=1, max_length=255, allow_blank=False, trim_whitespace=True)
    slug = serializers.SlugField(min_length=1, max_length=255, read_only=True)
    description = serializers.CharField(min_length=1, max_length=255, allow_blank=False, trim_whitespace=True)
    level = serializers.IntegerField(read_only=True)
    parent = serializers.SlugRelatedField(slug_field="name", allow_null=True, queryset=Category.objects.all())
    children = RecursiveField(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%d %b %Y, %H:%M")
    updated_at = serializers.DateTimeField(read_only=True, format="%d %b %Y, %H:%M")

    class Meta:
        model = Category
        fields = [
            "id", "name", "slug", "description", "level", "parent", "children", "products", "created_at", "updated_at",
        ]
        validators = [
            UniqueTogetherValidator(queryset=Category.objects.all(), fields=["name", "parent"])
        ]

    def validate(self, attrs):
        categoryName = attrs.get("name", "")
        parentName = attrs.get("parent", "")

        isCategoryFound = Category.objects.filter(name__iexact=categoryName, parent=None).exists()

        # Handling special condition where parent can be Null.
        # This is not handled by UniqueTogetherValidator as there is no check for type 'None' in db by the validator.
        if parentName is None and isCategoryFound:
            raise serializers.ValidationError({
                "message": "The fields name, parent must make a unique set."
            })

        return super().validate(attrs)

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category

class BrandSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=1, max_length=255, allow_blank=False, trim_whitespace=True)
    slug = serializers.SlugField(min_length=1, max_length=255, read_only=True)
    description = serializers.CharField(min_length=1, max_length=255, allow_blank=False, trim_whitespace=True)
    created_at = serializers.DateTimeField(read_only=True, format="%d %b %Y, %H:%M")
    updated_at = serializers.DateTimeField(read_only=True, format="%d %b %Y, %H:%M")

    class Meta:
        model = Brand
        fields = ["id", "name", "slug", "description", "created_at", "updated_at"]

    def validate(self, attrs):
        brandName = attrs.get("name", "")
        isBrandFound = Brand.objects.filter(name__iexact=brandName).exists()

        if isBrandFound:
            raise serializers.ValidationError({
                "message": "Brand '" + brandName + "' already exists and cannot be created or updated again."
            })

        return super().validate(attrs)

    def create(self, validated_data):
        brand = Brand.objects.create(**validated_data)
        return brand

class WishlistProductSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="brand.name", read_only = True)
    category = serializers.CharField(source="category.name", read_only = True)
    category_slug = serializers.CharField(source="category.slug", read_only = True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "description", "brand", "category", "category_slug"]
    
class WishListSerializer(serializers.ModelSerializer):
    product = WishlistProductSerializer(source="product_variant.product", read_only=True)
    product_variant = serializers.SlugRelatedField(slug_field="id", queryset=ProductVariant.objects.all())
    created_at = serializers.DateTimeField(read_only=True, format="%d %b %Y, %H:%M")
    updated_at = serializers.DateTimeField(read_only=True, format="%d %b %Y, %H:%M")

    class Meta:
        model = WishList
        fields = ["id", "product", "product_variant", "created_at", "updated_at"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        product_variant = attrs.get("product_variant", "")
        user = self.context.get("user", "")

        if WishList.objects.filter(product_variant=product_variant, user=user).exists():
            raise serializers.ValidationError("Product is already in wishlist.")

        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["product_variant"] = ProductVariantSerializer(instance=instance.product_variant).data
        return representation
