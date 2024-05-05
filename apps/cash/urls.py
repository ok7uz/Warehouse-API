from django.urls import path

from apps.cash.views import CashList, CashierList, SaleDetail, SaleList

app_name = 'cash'

urlpatterns = [
    path('', CashList.as_view(), name='cashs'),
    path('cashiers/', CashierList.as_view(), name='cashiers'),
    path('sales/', SaleList.as_view(), name='sales'),
    path('sales/<uuid:sale_id>/', SaleDetail.as_view(), name='sale-detail'),

]
