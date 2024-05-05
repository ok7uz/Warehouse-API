from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from drf_spectacular.utils import extend_schema_field

from apps.payment.models import Payment
from apps.payment.serializers import PaymentSerializer
from apps.product.models import Product
from apps.product.serializers import ProductSerializer
from apps.purchase.models import PurchaseProduct, Provider, Purchase
from apps.store.models import Store
from apps.store.serializers import StoreSerializer
from apps.warehouse.models import WarehouseProduct
from apps.warehouse.serializers import ProviderSerializer, WarehouseProductSerializer




class PurchaseProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    product = WarehouseProductSerializer(read_only=True)
    quantity = serializers.IntegerField(write_only=True)

    class Meta:
        model = PurchaseProduct
        fields = ['product_id', 'product', 'quantity']

    def create(self, validated_data):
        product = get_object_or_404(Product, id=validated_data.pop('product_id'))
        quantity = validated_data.pop('quantity', None)
        purchase = self.context['purchase']
        provider_id = purchase.provider_id
        store = self.context['store']

        for _ in range(quantity):
            warehouse_product = WarehouseProduct.objects.create(
                product=product,
                provider_id=provider_id,
                store=store
                )
            
            PurchaseProduct.objects.create(
                product=warehouse_product,
                purchase=purchase,
                **validated_data
            )
        
        return PurchaseProduct.objects.filter(product__product=product, purchase=purchase)


class PurchaseSerializer(serializers.ModelSerializer):
    purchase_id = serializers.UUIDField(source='id')
    store_id = serializers.UUIDField(source='store.id', write_only=True)
    store = StoreSerializer(read_only=True)
    provider_id = serializers.IntegerField(source='provider.id', write_only=True)
    provider = ProviderSerializer(read_only=True)
    products = PurchaseProductSerializer(many=True)

    class Meta:
        model = Purchase
        fields = ['purchase_id', 'store_id', 'store', 'to_consignment', 'products', 'provider_id',
                  'provider', 'invoice_number', 'currency', 'total', 'created', 'time']

    def create(self, validated_data):
        products = validated_data.pop('products', None)
        
        store_id = validated_data.pop('store')['id']
        store = get_object_or_404(Store, id=store_id)
        validated_data['store'] = store

        provider_id = validated_data.pop('provider')['id']
        provider = get_object_or_404(Provider, id=provider_id)
        validated_data['provider'] = provider

        purchase = Purchase.objects.create(**validated_data)

        for product in products:
            product_id = product['product_id']
            product['product_id'] = product_id
            purchase_product = PurchaseProductSerializer(data=product, context={'purchase': purchase, 'store': store})
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
        fields = ('id', 'provider', 'total', 'currency', 'paid', 'left', 'created', 'time')


class PurchaseHistorySerializer(serializers.ModelSerializer):
    provider = serializers.CharField(source='provider.name', read_only=True)

    class Meta:
        model = Purchase
        fields = ('id', 'provider', 'total', 'currency', 'created', 'time')


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
