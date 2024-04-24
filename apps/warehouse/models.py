from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.product.models import Product
from apps.purchase.models import Provider


class WarehouseProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(_('quantity'), default=0, blank=False)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

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