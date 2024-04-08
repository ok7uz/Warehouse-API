from django.urls import path

from apps.product.views import ProductListView, ProductView, InventoryListView, InventoryView


app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('<int:product_id>/', ProductView.as_view(), name='product-detail'),

    path('', InventoryListView.as_view(), name='inventories'),
    path('<int:inventory_id>/', InventoryView.as_view(), name='inventory-detail'),
]
