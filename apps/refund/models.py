import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.purchase.models import Provider
from apps.warehouse.models import WarehouseProduct


class Refund(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='refunds')
    created = models.CharField(max_length=256, verbose_name=_('created time'))
    time = models.DateTimeField(auto_now_add=True)
    invoice_number = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, choices=[('UZS', 'UZS'), ('USD', 'USD')], verbose_name=_('currency'))
    amount = models.FloatField()

    class Meta:
        db_table = 'refund'
        ordering = ['-created']
        verbose_name = _('refund')
        verbose_name_plural = _('refund')

    def __str__(self):
        return f'{self.provider.name}: {self.amount}'


class RefundProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    refund = models.ForeignKey(Refund, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(WarehouseProduct, on_delete=models.CASCADE)

    total = models.FloatField()

    created = models.DateTimeField(_('created time'), auto_now_add=True)
    modified = models.DateTimeField(_('modified time'), auto_now=True)

    class Meta:
        db_table = 'refund_product'
        ordering = ['-modified']
        verbose_name = _('refund product')
        verbose_name_plural = _('refund products')

    def __str__(self):
        return self.warehouse_product.product.name
