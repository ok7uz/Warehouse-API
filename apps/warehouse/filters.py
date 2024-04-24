import django_filters.rest_framework as filters

from apps.warehouse.models import WarehouseProduct


class WarehouseProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='product__name', lookup_expr='icontains')
    barcode = filters.NumberFilter(field_name='product__barcode', lookup_expr='icontains')

    class Meta:
        model = WarehouseProduct
        fields = {
            'product__currency': ['exact'],
        }
