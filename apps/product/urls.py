from django.urls import path

from apps.product.views import ProductListView, ProductView


app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('<int:product_id>/', ProductView.as_view(), name='product-detail'),

]
