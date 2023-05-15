from django_filters import FilterSet, CharFilter, NumberFilter
from .models import Product, Category

class ProductFilter(FilterSet):
    brand = CharFilter(field_name='brand__name', lookup_expr='iexact')
    category = CharFilter(method='filter_category_name', label='Category name')
    discount = NumberFilter(field_name='discount', lookup_expr='gte')

    class Meta:
        model = Product
        fields = {}

    def filter_category_name(self, queryset, name, value):
        return queryset.filter(
                    category__in=Category.objects.filter(name__iexact=value).get_descendants(include_self=True)
                )

class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {}