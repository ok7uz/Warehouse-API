from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.product.models import Product
from apps.product.serializers import ProductSerializer
from apps.purchase.serializers import ProviderSerializer
from apps.warehouse.models import WarehouseProduct


class WarehouseProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', write_only=True)
    product = ProductSerializer(read_only=True)
    provider = ProviderSerializer(read_only=True)
    quantity = serializers.IntegerField(required=True)
    purchasing_amount = serializers.FloatField(read_only=True)
    selling_amount = serializers.FloatField(read_only=True)

    class Meta:
        model = WarehouseProduct
        fields = ['product_id', 'product', 'quantity', 'purchasing_amount', 'selling_amount',
                  'discount', 'discount_price', 'created', 'modified', 'provider']

    def validate(self, attrs):
        product_id = attrs['product']['id']
        warehouse_product = WarehouseProduct.objects.filter(product__id=product_id)
        if warehouse_product.exists():
            raise serializers.ValidationError({'product_id': 'there is a warehouse product with this product_id'})
        return super().validate(attrs)

    def create(self, validated_data):
        product = get_object_or_404(Product, id=validated_data['product']['id'])
        quantity = validated_data['quantity']
        purchasing_amount = product.purchasing_price * quantity
        selling_amount = product.selling_price * quantity

        return WarehouseProduct.objects.create(
            product=product,
            quantity=quantity,
            purchasing_amount=purchasing_amount,
            selling_amount=selling_amount
        )
