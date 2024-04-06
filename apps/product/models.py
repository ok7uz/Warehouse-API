from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(_('name'), max_length=128)
    barcode = models.PositiveIntegerField(_('barcode'))
    id_code = models.PositiveIntegerField(_('ID code'))
    currency = models.CharField(_('currency'), max_length=3, choices=[('UZS', 'UZS'), ('USD', 'USD')])

    purchasing_price = models.PositiveIntegerField(_('purchasing price'))
    extra_charge = models.PositiveSmallIntegerField(_('extra charge'))
    selling_price = models.PositiveIntegerField(_('selling price'))

    created = models.DateTimeField(_('created time'), auto_now_add=True)
    modified = models.DateTimeField(_('modified time'), auto_now=True)

    class Meta:
        db_table = 'product'
        ordering = ['-modified']
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name
