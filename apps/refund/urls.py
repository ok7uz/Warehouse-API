from django.urls import path

from apps.refund.views import RefundListView

urlpatterns = [
    path('', RefundListView.as_view(), name='refund-list'),
]
