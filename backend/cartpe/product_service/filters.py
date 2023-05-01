from django_filters import FilterSet, CharFilter, NumberFilter
from .models import Product

class ProductFilter(FilterSet):
    brand = CharFilter(field_name='brand__name', lookup_expr='iexact')
    category = CharFilter(field_name='category__name', lookup_expr='iexact')
    discount = NumberFilter(field_name='discount', lookup_expr='gte')

    class Meta:
        model = Product
        fields = {}