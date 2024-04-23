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
    ordering = ['-quantity']


admin.site.register(Provider)
admin.site.register(Purchase)
admin.site.register(PurchaseProduct)
admin.site.register(Payment)
