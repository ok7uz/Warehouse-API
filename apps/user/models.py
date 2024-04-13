from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(max_length=150, null=False, blank=False, verbose_name=_("first name"))
    last_name = models.CharField(max_length=150, null=False, blank=False, verbose_name=_("last name"))
    image = models.ImageField(upload_to='user/', verbose_name=_('image'))

    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
