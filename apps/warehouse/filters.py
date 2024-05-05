import django_filters.rest_framework as filters

from apps.warehouse.models import WarehouseProduct


class WarehouseProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='product__name', lookup_expr='icontains')
    barcode = filters.CharFilter(field_name='barcode', lookup_expr='icontains')
    currency = filters.CharFilter(field_name='product__currency', lookup_expr='exact')
    provider_id = filters.CharFilter(field_name='provider__id', lookup_expr='exact')

    class Meta:
        model = WarehouseProduct
        fields = ['name', 'barcode', 'currency', 'provider_id']
