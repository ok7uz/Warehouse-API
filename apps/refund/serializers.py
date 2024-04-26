from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.purchase.models import Provider
from apps.purchase.serializers import ProviderSerializer
from apps.refund.models import Refund, RefundProduct
from apps.warehouse.models import WarehouseProduct
from apps.warehouse.serializers import WarehouseProductSerializer


class RefundProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', write_only=True)
    product = WarehouseProductSerializer(read_only=True)
    quantity = serializers.IntegerField(required=True)

    class Meta:
        model = RefundProduct
        fields = ['product_id', 'product', 'quantity', 'discount', 'discount_price', 'total']

    def create(self, validated_data):
        warehouse_product = get_object_or_404(WarehouseProduct, id=validated_data.pop('product')['id'])
        quantity = validated_data.pop('quantity', None)
        refund = self.context['refund']
        # provider_id = refund.provider_id
        # discount = validated_data.get('discount', None)
        # discount_price = validated_data.get('discount_price', None)

        warehouse_product.quantity -= quantity
        warehouse_product.purchasing_amount = warehouse_product.product.purchasing_price * warehouse_product.quantity
        warehouse_product.selling_amount = warehouse_product.product.selling_price * warehouse_product.quantity
        warehouse_product.save()

        return RefundProduct.objects.create(
            product=warehouse_product,
            refund=refund,
            quantity=quantity,
            **validated_data
        )

    class Meta:
        model = RefundProduct
        fields = '__all__'
    

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

        for product in products:
            product_id = product['product']['id']
            product['product_id'] = product_id
            refund_product = RefundProductSerializer(data=product, context={'refund': refund})
            refund_product.is_valid(raise_exception=True)
            refund_product.save()

        return refund
