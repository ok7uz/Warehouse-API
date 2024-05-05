import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.product.models import Product
from apps.store.models import Store


class Provider(models.Model):
    name = models.CharField(max_length=128)
    inn = models.PositiveIntegerField()
    contract_number = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class WarehouseProduct(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    barcode = models.CharField(max_length=16, blank=True)
    id_code = models.CharField(max_length=16, blank=True)

    is_avaiable = models.BooleanField(default=True)
    created = models.DateTimeField(_('created time'), auto_now_add=True)
    modified = models.DateTimeField(_('modified time'), auto_now=True)

    class Meta:
        db_table = 'warehouse_product'
        ordering = ['-modified']
        verbose_name = _('warehouse product')
        verbose_name_plural = _('warehouse products')

    def __str__(self):
        return self.product.name
    
    def save(self, *args, **kwargs):
        last_product = WarehouseProduct.objects.order_by('barcode').last()

        if not last_product:
            self.barcode = '7000000000001'
            self.id_code = '00001'
        elif not self.barcode:
            self.barcode = str(int(last_product.barcode) + 1)
            self.id_code = str(int(last_product.id_code) + 1).zfill(5)

        return super().save(*args, **kwargs)
