from django.contrib import admin

from apps.warehouse.models import WarehouseProduct


@admin.register(WarehouseProduct)
class WarehouseProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'purchasing_amount', 'selling_amount']
    readonly_fields = ['created', 'modified']
    search_fields = ['product']
    ordering = ['product']