from rest_framework import serializers

from apps.store.models import Store


class StoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Store
        fields = '__all__'
        