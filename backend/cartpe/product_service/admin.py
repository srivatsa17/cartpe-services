from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin
from .models import (
    Product,
    Category,
    Brand,
    ProductVariant,
    ProductVariantProperty,
    ProductVariantPropertyValue,
)


class EditLinkInLine(object):
    def edit(self, instance):
        url = reverse(
            f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
            args={instance.pk},
        )
        if instance.pk:
            link = mark_safe('<a href="{u}">edit</a>'.format(u=url))
            return link
        else:
            return ""


class ProductVariantInLine(EditLinkInLine, admin.TabularInline):
    model = ProductVariant
    readonly_fields = ("edit",)


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInLine]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantProperty)
admin.site.register(ProductVariantPropertyValue)
admin.site.register(Category, DraggableMPTTAdmin)
admin.site.register(Brand)
