from django.urls import path

from apps.purchase.views import (
    ProviderDetailView,
    ProviderListView,
    PurchaseListView,
    ConsignmentListView,
    PurchaseHistoryView
)

app_name = 'purchase'

urlpatterns = [
    path('', PurchaseListView.as_view(), name='purchases'),
    path('consignment/', ConsignmentListView.as_view(), name='consignment'),
    path('history/', PurchaseHistoryView.as_view(), name='history'),
    path('providers/', ProviderListView.as_view(), name='providers'),
    path('providers/<int:provider_id>/', ProviderDetailView.as_view(), name='provider-detail')
]
