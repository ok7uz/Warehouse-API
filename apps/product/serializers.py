from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.product.models import Product
from apps.store.models import Store


class ProductSerializer(serializers.ModelSerializer):
    store_id = serializers.UUIDField(source='store.id')

    class Meta:
        model = Product
        fields = [
            'id', "store_id", "name", "currency", "purchasing_price", "markup_percentage", "selling_price",
            "wholesale_price", "created", "modified",
        ]

    def create(self, validated_data):
        store = get_object_or_404(Store, id=validated_data.pop('store')['id'])
        return Product.objects.create(store=store, **validated_data)
