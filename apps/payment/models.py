import uuid
from django.db import models

from apps.purchase.models import Purchase


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=(('card', 'card'), ('cash', 'cash')))
    amount = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.purchase}: {self.amount}'
