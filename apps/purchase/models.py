import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.store.models import Store
from apps.warehouse.models import Provider, WarehouseProduct



class Purchase(models.Model):
    id = models.UUIDField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='purchases')
    created = models.CharField(max_length=256, verbose_name=_('created time'))
    time = models.DateTimeField(auto_now_add=True)
    invoice_number = models.PositiveIntegerField()
    to_consignment = models.BooleanField()
    currency = models.CharField(max_length=3, choices=[('UZS', 'UZS'), ('USD', 'USD')], verbose_name=_('currency'))

    total = models.FloatField()
    paid = models.FloatField(default=0)
    left = models.FloatField(default=0)

    class Meta:
        db_table = 'purchase'
        ordering = ['-created']
        verbose_name = _('purchase')
        verbose_name_plural = _('purchases')

    def save(self, *args, **kwargs):
        self.left = self.total - self.paid
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.provider.name}: {self.total}'


class PurchaseProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(WarehouseProduct, related_name='purchase_product', on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='products')

    created = models.DateTimeField(_('created time'), auto_now_add=True)
    modified = models.DateTimeField(_('modified time'), auto_now=True)

    class Meta:
        db_table = 'purchase_product'
        ordering = ['-modified']
        verbose_name = _('purchase product')
        verbose_name_plural = _('purchase products')

    def __str__(self):
        return self.product.name
