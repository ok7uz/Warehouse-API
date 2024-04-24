from django.contrib import admin

from apps.payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['purchase', 'type', 'amount', 'created']
    search_fields = ['purchase']
    list_filter = ['type']
    ordering = ['-created']