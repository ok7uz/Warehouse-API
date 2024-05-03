from django.contrib import admin

from apps.purchase.models import Purchase, PurchaseProduct, Provider


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['provider', 'total', 'paid', 'left', 'created']
    search_fields = ['provider']
    ordering = ['-created']


@admin.register(PurchaseProduct)
class PurchaseProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'purchase',  'created']
    readonly_fields = ['created', 'modified']
    search_fields = ['product']
    ordering = ['-created']


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'inn', 'contract_number']
    search_fields = ['name', 'inn']
    ordering = ['name']
