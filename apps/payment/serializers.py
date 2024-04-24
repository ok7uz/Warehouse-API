from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.payment.models import Payment
from apps.purchase.models import Purchase


class PaymentSerializer(serializers.ModelSerializer):
    purchase_id = serializers.UUIDField(source='purchase.id')

    class Meta:
        model = Payment
        fields = ('id', 'purchase_id', 'type', 'amount', 'created')

    def create(self, validated_data):
        purchase = get_object_or_404(Purchase, id=validated_data.pop('purchase')['id'])
        validated_data['purchase'] = purchase
        purchase.paid += validated_data['amount']
        purchase.save()

        return super().create(validated_data)
