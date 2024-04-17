from rest_framework import serializers

from apps.product.models import WarehouseProduct, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class WarehouseProductSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Product.objects.all())

    class Meta:
        model = WarehouseProduct
        fields = '__all__'
