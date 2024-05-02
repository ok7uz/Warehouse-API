from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from apps.purchase.filters import ProviderFilter, PurchaseFilter
from apps.purchase.models import Provider, Purchase
from apps.store.models import Store
from apps.store.serializers import StoreSerializer


class StoreListView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={200: StoreSerializer(many=True)},
        tags=['Store']
    )
    def get(self, request):
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=StoreSerializer,
        responses={200: StoreSerializer},
        tags=['Store']
    )
    def post(self, request):
        serializer = StoreSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StoreDetailView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={200: StoreSerializer},
        tags=['Store']
    )
    def get(self, request, store_id):
        store = get_object_or_404(Provider, id=store_id)
        serializer = StoreSerializer(store, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
