from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.purchase.filters import ProviderFilter
from apps.purchase.models import Provider, Purchase
from apps.purchase.serializers import ProviderDetailSerializer, ProviderSerializer, ConsignmentSerializer, PurchaseSerializer


class ProviderListView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter('search', location=OpenApiParameter.QUERY, type=OpenApiTypes.STR,
                             description='searching ...'),
        ],
        responses={200: ProviderSerializer(many=True)},
        tags=['Purchase']
    )
    def get(self, request):
        providers = Provider.objects.all()
        provider_filter = ProviderFilter(request.GET, queryset=providers)
        queryset = provider_filter.qs if provider_filter.is_valid() else providers.none()
        serializer = ProviderSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=ProviderSerializer,
        responses={200: ProviderSerializer},
        tags=['Purchase']
    )
    def post(self, request):
        serializer = ProviderSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProviderDetailView(APIView):
    @extend_schema(
        responses={200: ProviderDetailSerializer},
        tags=['Purchase']
    )
    def get(self, request, provider_id):
        provider = get_object_or_404(Provider, id=provider_id)
        serializer = ProviderDetailSerializer(provider, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



class PurchaseListView(APIView):

    @extend_schema(
        request=PurchaseSerializer,
        responses={200: PurchaseSerializer},
        tags=['Purchase']
    )
    def post(self, request):
        serializer = PurchaseSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsignmentListView(APIView):

    @extend_schema(
        responses={200: ConsignmentSerializer(many=True)},
        tags=['Purchase']
    )
    def get(self, request):
        queryset = Purchase.objects.all()
        serializer = ConsignmentSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

