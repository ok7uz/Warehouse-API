from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from apps.warehouse.filters import WarehouseProductFilter
from apps.warehouse.models import WarehouseProduct
from apps.warehouse.serializers import WarehouseProductSerializer


class WarehouseProductListView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = WarehouseProductSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter('page', location=OpenApiParameter.QUERY, type=OpenApiTypes.INT),
            OpenApiParameter('page_size', location=OpenApiParameter.QUERY, type=OpenApiTypes.INT),
            OpenApiParameter('search', location=OpenApiParameter.QUERY, type=OpenApiTypes.STR,
                             description='via name, barcode'),
            OpenApiParameter('product__currency', location=OpenApiParameter.QUERY, type=OpenApiTypes.STR),
            OpenApiParameter('name', location=OpenApiParameter.QUERY, type=OpenApiTypes.STR),
            OpenApiParameter('barcode', location=OpenApiParameter.QUERY, type=OpenApiTypes.STR),
            OpenApiParameter('provider_id', location=OpenApiParameter.QUERY, type=OpenApiTypes.INT32),
        ],
        responses={200: WarehouseProductSerializer(many=True)},
        tags=['Warehouse Product']
    )
    def get(self, request):
        products = WarehouseProduct.objects.filter(is_avaiable=True)
        search = request.query_params.get('search', None)
        products = products.filter(
            Q(product__name__icontains=search) | Q(product__barcode__icontains=search)) if search else products

        product_filter = WarehouseProductFilter(request.GET, queryset=products)
        queryset = product_filter.qs if product_filter.is_valid() else products.none()
        serializer =  WarehouseProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=WarehouseProductSerializer,
        responses={200: WarehouseProductSerializer},
        tags=['Warehouse Product']
    )
    def post(self, request):
        print('9999')
        serializer = WarehouseProductSerializer(data=request.data)
        print('0000')

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'data': data,
        })
