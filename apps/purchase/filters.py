import django_filters.rest_framework as filters

from apps.purchase.models import Provider


class ProviderFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Provider
        fields = ('search',)
