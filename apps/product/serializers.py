from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.product.models import Payment, Provider, Purchase, PurchaseProduct, WarehouseProduct, Product
from apps.user.serializers import UserSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class WarehouseProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', write_only=True)
    product = ProductSerializer(read_only=True)
    quantity = serializers.IntegerField(required=True)
    purchasing_amount = serializers.FloatField(read_only=True)
    selling_amount = serializers.FloatField(read_only=True)

    class Meta:
        model = WarehouseProduct
        fields = ['product_id', 'product', 'quantity', 'purchasing_amount', 'selling_amount', 'created', 'modified']

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
    

class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = '__all__'


class PurchaseProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', write_only=True)
    product = ProductSerializer(read_only=True)
    quantity = serializers.IntegerField(required=True)

    class Meta:
        model = PurchaseProduct
        fields = ['product_id', 'product', 'quantity', 'discount', 'discount_price', 'total']

    def create(self, validated_data):
        product = get_object_or_404(Product, id=validated_data.pop('product')['id'])
        quantity = validated_data.pop('quantity', None)
        purchase = self.context['purchase']    

        warehouse_product, created = WarehouseProduct.objects.get_or_create(product=product)
        warehouse_product.quantity += quantity
        warehouse_product.purchasing_amount = warehouse_product.product.purchasing_price * warehouse_product.quantity
        warehouse_product.selling_amount = warehouse_product.product.selling_price * warehouse_product.quantity
        warehouse_product.save()

        return PurchaseProduct.objects.create(
            product=product,
            purchase=purchase,
            quantity=quantity,
            **validated_data
        )


class PurchaseSerializer(serializers.ModelSerializer):
    provider_id = serializers.IntegerField(source='provider.id', write_only=True)
    provider = ProviderSerializer(read_only=True)
    products = PurchaseProductSerializer(many=True)

    class Meta:
        model = Purchase
        fields = ['id', 'products', 'provider_id', 'provider', 'total', 'created']

    def create(self, validated_data):
        products = validated_data.pop('products', None)
        provider_id = validated_data.pop('provider')['id']
        validated_data['provider_id'] = provider_id

        purchase = Purchase.objects.create(**validated_data)        

        for product in products:
            product_id = product['product']['id']
            product['product_id'] = product_id
            purchase_product = PurchaseProductSerializer(data=product, context={'purchase': purchase})
            purchase_product.is_valid(raise_exception=True)
            purchase_product.save()

        return purchase 

class ConsignmentSerializer(serializers.ModelSerializer):
    provider = serializers.CharField(source='provider.name', read_only=True)

    class Meta:
        model = Purchase
        fields = ('id', 'created', 'provider', 'total', 'paid', 'left', 'comment')       


class PaymentSerializer(serializers.ModelSerializer):
    purchase_id = serializers.IntegerField(source='purchase.id')

    class Meta:
        model = Payment
        fields = ('id', 'purchase_id', 'type', 'amount')    

    def create(self, validated_data):
        purchase = get_object_or_404(Purchase, id=validated_data.pop('purchase')['id'])
        validated_data['purchase'] = purchase
        purchase.paid += validated_data['amount']
        purchase.save()

        return super().create(validated_data)   
