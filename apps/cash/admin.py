from django.contrib import admin

from apps.cash.models import Sale, SaleProduct, Cash, Cashier


admin.site.register(Sale)
admin.site.register(SaleProduct)
admin.site.register(Cash)
admin.site.register(Cashier)

