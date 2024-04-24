from django.urls import path

from apps.payment.views import PaymentListView

app_name = 'payment'

urlpatterns = [
    path('', PaymentListView.as_view(), name='payments'),
]
