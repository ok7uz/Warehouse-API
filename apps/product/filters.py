from apps.product.models import Product, WarehouseProduct
import django_filters.rest_framework as filters


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'currency': ['exact'], 
            'name': ['icontains'],
        }


class WarehouseProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='product__name', lookup_expr='icontains')
    barcode = filters.NumberFilter(field_name='product__barcode', lookup_expr='icontains')

    class Meta:
        model = WarehouseProduct
        fields = {
            'product__currency': ['exact'], 
            # 'name': ['icontains'],
            # 'barcode': ['icontains'],
        }

