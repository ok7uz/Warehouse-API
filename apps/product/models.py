from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.user.models import User


class Product(models.Model):
    name = models.CharField(_('name'), max_length=128)
    barcode = models.PositiveIntegerField(_('barcode'))
    id_code = models.PositiveIntegerField(_('ID code'))
    currency = models.CharField(_('currency'), max_length=3, choices=[('UZS', 'UZS'), ('USD', 'USD')])

    purchasing_price = models.PositiveIntegerField(_('purchasing price'))
    markup_percentage = models.PositiveSmallIntegerField(_('extra charge'), default=0)
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
    

class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    quantity = models.IntegerField(_('quantity'), default=0)

    purchasing_price = models.PositiveIntegerField(_('purchasing price'))
    markup_percentage = models.PositiveSmallIntegerField(_('extra charge'), default=0)
    selling_price = models.PositiveIntegerField(_('selling price'))

    created = models.DateTimeField(_('created time'), auto_now_add=True)
    modified = models.DateTimeField(_('modified time'), auto_now=True)

    class Meta:
        db_table = 'inventory'
        ordering = ['-modified']
        verbose_name = _('inventory')
        verbose_name_plural = _('inventories')

    def __str__(self):
        return self.product.name


class Purchase(models.Model):
    supplier = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('quantity'))
    date = models.DateField(_('created date'), auto_now_add=True)

    class Meta:
        db_table = 'purchase'
        verbose_name = _('Purchase')
        verbose_name_plural = _('Purchases')

    def __str__(self):
        pass
