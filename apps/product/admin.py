from django.contrib import admin

from apps.product.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'barcode', 'id_code', 'currency', 'purchasing_price', 'markup_percentage', 'selling_price']
    list_filter = ['currency', 'modified']
    search_fields = ['name']
