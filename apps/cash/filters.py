import django_filters.rest_framework as filters

from apps.cash.models import Cashier


class CashierFilter(filters.FilterSet):
    cash_id = filters.UUIDFilter(field_name='cash__id', lookup_expr='exact')

    class Meta:
        model = Cashier
        fields = ['cash_id']


class SaleFilter(filters.FilterSet):
    cash_id = filters.UUIDFilter(field_name='cash__id', lookup_expr='exact')
    cashier_id = filters.UUIDFilter(field_name='cashier__id', lookup_expr='exact')

    class Meta:
        model = Cashier
        fields = ['cash_id', 'cashier_id']
