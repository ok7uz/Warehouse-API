from apps.product.models import Product, WarehouseProduct
from django_filters.rest_framework import FilterSet


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'currency': ['exact'], 
            'name': ['icontains'],
        }


class WarehouseProductFilter(FilterSet):
    class Meta:
        model = WarehouseProduct
        fields = {
            'product__currency': ['exact'], 
        }
