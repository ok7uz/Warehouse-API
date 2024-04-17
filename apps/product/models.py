from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.user.models import User


class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('name'))
    barcode = models.PositiveIntegerField(verbose_name=_('barcode'))
    id_code = models.PositiveIntegerField(verbose_name=_('ID code'))
    currency = models.CharField(max_length=3, choices=[('UZS', 'UZS'), ('USD', 'USD')], verbose_name=_('currency'))

    purchasing_price = models.FloatField(verbose_name=_('purchasing price'))
    markup_percentage = models.PositiveSmallIntegerField(verbose_name=_('markup percentage'))
    selling_price = models.FloatField(verbose_name=_('selling price'))
    wholesale_price = models.FloatField(verbose_name=_('wholesale price'))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created time'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified time'))

    class Meta:
        db_table = 'product'
        ordering = ['-modified']
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name
    

class WarehouseProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    quantity = models.IntegerField(_('quantity'), default=0, blank=False)

    purchasing_amount = models.PositiveIntegerField(_('purchasing amount'))
    selling_amount = models.PositiveIntegerField(_('selling amount'))

    created = models.DateTimeField(_('created time'), auto_now_add=True)
    modified = models.DateTimeField(_('modified time'), auto_now=True)

    class Meta:
        db_table = 'warehouse_product'
        ordering = ['-modified']
        verbose_name = _('warehouse product')
        verbose_name_plural = _('warehouse products')

    def __str__(self):
        return self.product.name
