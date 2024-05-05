from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.cash.models import Cash, Cashier, Sale, SaleProduct
from apps.warehouse.models import WarehouseProduct
from apps.warehouse.serializers import WarehouseProductSerializer


class SaleProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    product = WarehouseProductSerializer(read_only=True)

    class Meta:
        model = SaleProduct
        fields = ('id', 'product', 'product_id')

    def create(self, validated_data):
        sale = self.context['sale']
        product = get_object_or_404(WarehouseProduct, id=validated_data.pop('product_id'))
        product.is_avaiable = False
        product.save()
        return SaleProduct.objects.create(product=product, sale=sale, **validated_data)


class SaleSerializer(serializers.ModelSerializer):
    cash_id = serializers.UUIDField(source='cash.id')
    cashier_id = serializers.UUIDField(source='cashier.id')
    products = SaleProductSerializer(many=True)

    class Meta:
        model = Sale
        fields = ('id', 'cash_id', 'cashier_id', 'total', 'products')

    def create(self, validated_data):
        cash = get_object_or_404(Cash, id=validated_data.pop('cash')['id'])
        cashier = get_object_or_404(Cashier, id=validated_data.pop('cashier')['id'])
        products = validated_data.pop('products')
        sale = Sale.objects.create(cash=cash, cashier=cashier, **validated_data)

        serializer = SaleProductSerializer(data=products, many=True, context={'sale': sale})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return sale


class CashierSerializer(serializers.ModelSerializer):
    cash_id = serializers.UUIDField(source='cash.id')

    class Meta:
        model = Cashier
        fields = ('id', 'name', 'cash_id')

    def create(self, validated_data):
        cash = get_object_or_404(Cash, id=validated_data.pop('cash')['id'])
        return Cashier.objects.create(cash=cash, **validated_data)
    

class CashSerializer(serializers.ModelSerializer):
    cashiers = CashierSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cash
        fields = ('id', 'name', 'cashiers')
