from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150, null=False, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, null=False, blank=False)
    image = models.ImageField(_('image'), upload_to="user/")

    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
