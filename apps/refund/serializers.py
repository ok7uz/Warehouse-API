from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.purchase.models import Provider
from apps.purchase.serializers import ProviderSerializer
from apps.refund.models import Refund, RefundProduct
from apps.warehouse.models import WarehouseProduct
from apps.warehouse.serializers import WarehouseProductSerializer


class RefundProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', write_only=True)
    warehouse_product = WarehouseProductSerializer(read_only=True)

    class Meta:
        model = RefundProduct
        fields = ['product_id', 'warehouse_product', 'total']

    def create(self, validated_data):
        warehouse_product = get_object_or_404(WarehouseProduct, id=validated_data.pop('product')['id'])
        refund = self.context['refund']

        warehouse_product.is_avaiable = False
        warehouse_product.save()

        return RefundProduct.objects.create(
            product=warehouse_product,
            refund=refund,
            **validated_data
        )
    

class RefundSerializer(serializers.ModelSerializer):
    products = RefundProductSerializer(many=True)
    provider_id = serializers.IntegerField(source='provider.id', write_only=True)
    provider = ProviderSerializer(read_only=True)

    class Meta:
        model = Refund
        fields = '__all__'

    def create(self, validated_data):
        products = validated_data.pop('products', None)
        provider_id = validated_data.pop('provider')['id']
        provider = get_object_or_404(Provider, id=provider_id)
        validated_data['provider'] = provider
        refund = Refund.objects.create(**validated_data)
        amount = validated_data.get('amount')
        product_one = get_object_or_404(WarehouseProduct, id=products[0]['product']['id'])
        purchase = product_one.purchase_product.purchase

        for product in products:
            product_id = product['product']['id']
            product['product_id'] = product_id
            refund_product = RefundProductSerializer(data=product, context={'refund': refund})
            refund_product.is_valid(raise_exception=True)
            refund_product.save()

        purchase.total -= amount
        purchase.save()

        return refund
