from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from drf_spectacular.utils import extend_schema_field

from apps.payment.models import Payment
from apps.payment.serializers import PaymentSerializer
from apps.product.models import Product
from apps.product.serializers import ProductSerializer
from apps.purchase.models import PurchaseProduct, Provider, Purchase
from apps.warehouse.models import WarehouseProduct


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
        provider_id = purchase.provider_id

        warehouse_product = WarehouseProduct.objects.filter(product=product, provider_id=provider_id)
        if not warehouse_product.exists():
            warehouse_product = WarehouseProduct(product=product, provider_id=provider_id, quantity=0)
        else:
            warehouse_product = warehouse_product.first()

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
    purchase_id = serializers.UUIDField(source='id')
    provider_id = serializers.IntegerField(source='provider.id', write_only=True)
    provider = ProviderSerializer(read_only=True)
    products = PurchaseProductSerializer(many=True)

    class Meta:
        model = Purchase
        fields = ['purchase_id', 'to_consignment', 'products', 'provider_id', 'provider',
                  'invoice_number', 'total', 'created', 'time']

    def create(self, validated_data):
        products = validated_data.pop('products', None)
        provider_id = validated_data.pop('provider')['id']
        provider = get_object_or_404(Provider, id=provider_id)
        validated_data['provider'] = provider
        purchase = Purchase.objects.create(**validated_data)

        for product in products:
            product_id = product['product']['id']
            product['product_id'] = product_id
            purchase_product = PurchaseProductSerializer(data=product, context={'purchase': purchase})
            purchase_product.is_valid(raise_exception=True)
            purchase_product.save()

        return purchase
    

class PurchaseInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = ['id', 'to_consignment', 'invoice_number', 'total', 'created', 'time']


class ConsignmentSerializer(serializers.ModelSerializer):
    provider = serializers.CharField(source='provider.name', read_only=True)

    class Meta:
        model = Purchase
        fields = ('id', 'provider', 'total', 'paid', 'left', 'comment', 'created', 'time')


class ProviderDetailSerializer(serializers.ModelSerializer):
    purchases = PurchaseInfoSerializer(many=True)
    payments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Provider
        fields = ['name', 'inn', 'contract_number', 'purchases', 'payments']

    @extend_schema_field(PaymentSerializer(many=True))
    def get_payments(self, provider):
        payments = Payment.objects.filter(purchase__provider=provider)
        return PaymentSerializer(payments, many=True).data
