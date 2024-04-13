from django.contrib import admin

from apps.product.models import Product, Inventory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'barcode', 'id_code', 'currency', 'purchasing_price', 'markup_percentage', 'selling_price']
    readonly_fields = ['created', 'modified']
    list_filter = ['currency', 'modified']
    search_fields = ['name']


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'purchasing_price', 'markup_percentage', 'selling_price']
    readonly_fields = ['created', 'modified']
    search_fields = ['product']
    ordering = ['-quantity']
