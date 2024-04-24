import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.product.models import Product


class Provider(models.Model):
    name = models.CharField(max_length=128)
    inn = models.PositiveIntegerField()
    contract_number = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Purchase(models.Model):
    id = models.UUIDField(primary_key=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    created = models.CharField(max_length=256, verbose_name=_('created time'))
    time = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=256, null=True)
    invoice_number = models.PositiveIntegerField()
    to_consignment = models.BooleanField()

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField(_('quantity'), default=0, blank=False)

    discount = models.IntegerField()
    discount_price = models.FloatField()
    total = models.FloatField()

    created = models.DateTimeField(_('created time'), auto_now_add=True)
    modified = models.DateTimeField(_('modified time'), auto_now=True)

    class Meta:
        db_table = 'purchase_product'
        ordering = ['-modified']
        verbose_name = _('purchase product')
        verbose_name_plural = _('purchase products')

    def __str__(self):
        return self.product.name
