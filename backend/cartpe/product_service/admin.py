from django.contrib import admin
from .models import (
    Product,
    Image,
    Category,
)

# Register your models here.

admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Category)