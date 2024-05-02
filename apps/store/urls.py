from django.urls import path

from apps.purchase.views import (
    ProviderDetailView,
    ProviderListView,
    PurchaseListView,
    ConsignmentListView,
    PurchaseHistoryView
)
from apps.store.views import StoreDetailView, StoreListView

app_name = 'store'

urlpatterns = [
    path('', StoreListView.as_view(), name='stores'),
    path('<uuid:store_id>/', StoreDetailView.as_view(), name='store-detail'),
]
