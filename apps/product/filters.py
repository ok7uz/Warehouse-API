from apps.product.models import Product
import django_filters.rest_framework as filters


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    barcode = filters.CharFilter(lookup_expr='icontains')
    currency = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['name', 'barcode', 'currency']
