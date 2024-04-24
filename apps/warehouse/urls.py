from django.urls import path, include

from apps.warehouse.views import WarehouseProductListView

app_name = 'warehouse'

urlpatterns = [
    path('', WarehouseProductListView.as_view(), name='warehouse-products'),
]
