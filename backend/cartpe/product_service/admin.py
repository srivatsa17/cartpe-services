from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import (
    Product, Image, Category, Brand, Attribute, AttributeValue
)

# Register your models here.

admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Category, DraggableMPTTAdmin)
admin.site.register(Brand)
admin.site.register(Attribute)
admin.site.register(AttributeValue)