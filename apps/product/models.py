from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('name'))
    barcode = models.CharField(max_length=128, verbose_name=_('barcode'))
    id_code = models.PositiveIntegerField(verbose_name=_('ID code'))
    currency = models.CharField(max_length=3, choices=[('UZS', 'UZS'), ('USD', 'USD')], verbose_name=_('currency'))

    purchasing_price = models.FloatField(verbose_name=_('purchasing price'))
    markup_percentage = models.FloatField(verbose_name=_('markup percentage'))
    selling_price = models.FloatField(verbose_name=_('selling price'))
    wholesale_price = models.FloatField(verbose_name=_('wholesale price'), null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created time'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified time'))

    class Meta:
        db_table = 'product'
        ordering = ['-modified']
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name
    


