from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.product.models import Product
from apps.product.serializers import ProductSerializer
from apps.warehouse.models import Provider, WarehouseProduct


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = '__all__'


class WarehouseProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id')
    product_name = serializers.CharField(source='product.name', read_only=True)
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    provider_id = serializers.IntegerField(source='provider.id', read_only=True)
    product = ProductSerializer(read_only=True)
    provider = ProviderSerializer(read_only=True)

    class Meta:
        model = WarehouseProduct
        fields = ['id', 'product_id', 'product_name', 'product', 'barcode', 'id_code',
                  'created', 'modified', 'provider_id', 'provider_name', 'provider']

    def validate(self, attrs):
        product_id = attrs['product']['id']
        warehouse_product = WarehouseProduct.objects.filter(product__id=product_id)
        if warehouse_product.exists():
            raise serializers.ValidationError({'product_id': 'there is a warehouse product with this product_id'})
        return super().validate(attrs)

    def create(self, validated_data):
        product = get_object_or_404(Product, id=validated_data['product']['id'])

        return WarehouseProduct.objects.create(
            product=product,
        )
