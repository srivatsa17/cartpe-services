from django.db import models
import uuid
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length = 255, null = False, blank = False)
    slug = models.SlugField(max_length = 255, null = True, blank = True)
    description = models.TextField(null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Product(models.Model):
    sku = models.UUIDField(primary_key = False, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 255, unique = True, null = False, blank = False)
    slug = models.SlugField(max_length = 255, null = True, blank = True)
    description = models.TextField(null = False, blank = False)
    price = models.DecimalField(max_digits = 7, decimal_places = 2, null = False, blank = False)
    brand = models.CharField(max_length = 255, null = False, blank = False)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True, blank = True)
    discount = models.PositiveSmallIntegerField(default = 0, null = False, blank = False)
    stock_count = models.PositiveIntegerField(default = 0, null = False, blank = False)
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
    product = models.ForeignKey(Product, on_delete = models.CASCADE, null = False, blank = False)
    image = models.ImageField(max_length = 255, null = False, blank = False)
    is_featured = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
