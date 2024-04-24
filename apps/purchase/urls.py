from django.urls import path

from apps.purchase.views import ProviderListView, PurchaseListView, ConsignmentListView

app_name = 'purchase'

urlpatterns = [
    path('', PurchaseListView.as_view(), name='purchases'),
    path('consignment/', ConsignmentListView.as_view(), name='consignment'),
    path('providers/', ProviderListView.as_view(), name='providers'),
]
