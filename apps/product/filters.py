from apps.product.models import Product
import django_filters.rest_framework as filters


class ProductFilter(filters.FilterSet):

    class Meta:
        model = Product
        fields = {
            'currency': ['exact'], 
            'name': ['icontains'],
            'barcode': ['icontains'],
        }
