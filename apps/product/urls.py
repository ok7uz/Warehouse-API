from django.urls import path, include

from apps.product.views import ProductListView, ProductView, ProviderListView, PurchaseListView, WarehouseProductListView


app_name = 'product'

urlpatterns = [
    path('products/', include([
        path('', ProductListView.as_view(), name='products'),
        path('<int:product_id>/', ProductView.as_view(), name='product-detail'),
    ])),
    path('warehouse/', include([
        path('', WarehouseProductListView.as_view(), name='warehouse-products'),
    ])),
    path('providers/', ProviderListView.as_view(), name='providers'),
    path('purchase/', PurchaseListView.as_view(), name='purchases')
]
