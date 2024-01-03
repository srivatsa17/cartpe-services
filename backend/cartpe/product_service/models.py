from django.db import models
import uuid
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    name = models.CharField(max_length = 255, null = False, blank = False)
    slug = models.SlugField(max_length = 255, null = True, blank = True)
    description = models.TextField(null = False, blank = False)
    parent = TreeForeignKey('self', on_delete = models.CASCADE, blank = False, null = True, related_name = 'children')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        unique_together = [['name', 'parent'], ]
        verbose_name_plural = "categories"

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.parent:
            self.slug = slugify("%s %s" % (self.parent.get_root(), self.name))
        else:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Brand(models.Model):
    name = models.CharField(max_length = 255, unique = True, null = False, blank = False)
    slug = models.SlugField(max_length = 255, null = True, blank = True)
    description = models.TextField(null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)

class Attribute(models.Model):
    name = models.CharField(max_length = 255, null = True, blank = True)

    def __str__(self) -> str:
        return self.name

class AttributeValue(models.Model):
    value = models.CharField(max_length = 255, null = True, blank = True)
    attribute = models.ForeignKey(Attribute, on_delete = models.CASCADE, null = True, blank = True, related_name = 'attribute_values')

    def __str__(self) -> str:
        return self.value

class Product(models.Model):
    sku = models.UUIDField(primary_key = False, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 255, unique = True, null = False, blank = False)
    slug = models.SlugField(max_length = 255, null = True, blank = True)
    description = models.TextField(null = False, blank = False)
    price = models.DecimalField(max_digits = 7, decimal_places = 2, null = False, blank = False)
    brand = models.ForeignKey(Brand, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'products')
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'products')
    discount = models.PositiveSmallIntegerField(default = 0, null = False, blank = False)
    stock_count = models.PositiveIntegerField(default = 0, null = False, blank = False)
    attributes = models.ManyToManyField(Attribute, blank = True, related_name = 'products')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    @property
    def discounted_price(self):
        return round(((self.price * self.discount) / 100), 2)

    @property
    def selling_price(self):
        return (self.price - self.discounted_price)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, null = False, blank = False, related_name = 'product_images')
    image = models.URLField(max_length = 255, null = False, blank = False)
    is_featured = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.image.url)