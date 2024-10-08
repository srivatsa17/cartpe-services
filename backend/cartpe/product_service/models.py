from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from mptt.models import MPTTModel, TreeForeignKey
from auth_service.models import User
from django.db.models import Avg


class Category(MPTTModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    description = models.TextField(null=False, blank=False)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, blank=False, null=True, related_name="children"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [
            ["name", "parent"],
        ]
        verbose_name_plural = "categories"

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.parent:
            parent_name = str(self.parent.get_root())
            # Check if the category name starts with the parent's name
            if self.name.lower().startswith(parent_name.lower()):
                self.slug = slugify(self.name)
            else:
                self.slug = slugify("%s %s" % (parent_name, self.name))
        else:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    description = models.TextField(null=False, blank=False)
    image = models.URLField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)


class ProductVariantProperty(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class ProductVariantPropertyValue(models.Model):
    value = models.CharField(max_length=255, null=True, blank=True)
    property = models.ForeignKey(
        ProductVariantProperty,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="product_variant_property_values",
    )

    def __str__(self) -> str:
        return "%s - %s" % (self.property.name, self.value)


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    description = models.TextField(null=False, blank=False)
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name="products"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    """
    This function is used to get the product rating average by using the reverse lookup for product_reviews
    which is a related name to `Product` model from `ProductReview` model.
    This function is used by `ProductSerializer` and `ProductRatingSerializer`
    """

    def rating_average(self):
        average_rating = self.product_reviews.aggregate(Avg("rating"))["rating__avg"]
        if average_rating is None:
            return 0
        return int(average_rating) if average_rating.is_integer() else round(average_rating, 2)

    """
    This function is used to get the product rating count by using the reverse lookup for product_reviews
    which is a related name to `Product` model from `ProductReview` model.
    This function is used by `ProductSerializer` and `ProductRatingSerializer`
    """

    def rating_count(self):
        return self.product_reviews.count()


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, blank=False, related_name="product_variants"
    )
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    sku = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    images = ArrayField(models.URLField(max_length=255, null=False, blank=False))
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False)
    discount = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    stock_count = models.PositiveIntegerField(default=0, null=False, blank=False)
    properties = models.ManyToManyField(
        ProductVariantPropertyValue, blank=True, related_name="product_variants"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def discounted_price(self):
        return round(((self.price * self.discount) / 100), 2)

    @property
    def selling_price(self):
        return self.price - self.discounted_price

    def __str__(self):
        return str(self.name)


class WishList(models.Model):
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, null=False, blank=False, related_name="wishlist"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False, related_name="wishlist"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, blank=False, related_name="product_reviews"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False, related_name="product_reviews"
    )
    headline = models.CharField(max_length=255, null=False, blank=False)
    rating = models.PositiveSmallIntegerField(
        null=False, blank=False, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)
