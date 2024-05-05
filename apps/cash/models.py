import uuid
from django.db import models

from apps.warehouse.models import WarehouseProduct


class Cash(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)


class Cashier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    cash = models.ForeignKey(Cash, on_delete=models.CASCADE, related_name='cashiers')


class Sale(models.Model):
    cash = models.ForeignKey(Cash, on_delete=models.CASCADE, related_name='sales')
    cashier = models.ForeignKey(Cashier, on_delete=models.CASCADE, related_name='sales')
    total = models.FloatField()


class SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(WarehouseProduct, on_delete=models.CASCADE, related_name='sale_products')