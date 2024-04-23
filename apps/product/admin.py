from django.contrib import admin

from apps.product.models import Product, Provider, WarehouseProduct, Purchase, PurchaseProduct, Payment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'barcode', 'id_code', 'currency', 'purchasing_price', 'markup_percentage', 'selling_price']
    readonly_fields = ['created', 'modified']
    list_filter = ['currency', 'modified']
    search_fields = ['name']


@admin.register(WarehouseProduct)
class WarehouseProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'purchasing_amount', 'selling_amount']
    readonly_fields = ['created', 'modified']
    search_fields = ['product']
    ordering = ['product']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['provider', 'total', 'paid', 'left', 'created']
    search_fields = ['provider']
    ordering = ['-created']


@admin.register(PurchaseProduct)
class PurchaseProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'purchase', 'quantity', 'created']
    readonly_fields = ['created', 'modified']
    search_fields = ['product']
    ordering = ['-created']


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'inn', 'contract_number']
    search_fields = ['name', 'inn']
    ordering = ['name']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['purchase', 'type', 'amount', 'created']
    search_fields = ['purchase']
    list_filter = ['type']
    ordering = ['-created']

