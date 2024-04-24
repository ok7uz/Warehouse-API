from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.warehouse.filters import WarehouseProductFilter
from apps.warehouse.models import WarehouseProduct
from apps.warehouse.serializers import WarehouseProductSerializer


class WarehouseProductListView(APIView, PageNumberPagination):
    serializer_class = WarehouseProductSerializer
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

    @extend_schema(
        parameters=[
            OpenApiParameter('page', location=OpenApiParameter.QUERY, type=OpenApiTypes.INT),
            OpenApiParameter('page_size', location=OpenApiParameter.QUERY, type=OpenApiTypes.INT),
            OpenApiParameter('search', location=OpenApiParameter.QUERY, type=OpenApiTypes.STR,
                             description='via name, barcode'),
            OpenApiParameter('product__currency', location=OpenApiParameter.QUERY, type=OpenApiTypes.STR),
            OpenApiParameter('name', location=OpenApiParameter.QUERY, type=OpenApiTypes.STR),
            OpenApiParameter('barcode', location=OpenApiParameter.QUERY, type=OpenApiTypes.STR),
        ],
        responses={200: WarehouseProductSerializer(many=True)},
        tags=['Warehouse Product']
    )
    def get(self, request):
        products = WarehouseProduct.objects.all()
        search = request.query_params.get('search', None)
        products = products.filter(
            Q(product__name__icontains=search) | Q(product__barcode__icontains=search)) if search else products

        product_filter = WarehouseProductFilter(request.GET, queryset=products)
        queryset = product_filter.qs if product_filter.is_valid() else products.none()
        page = self.paginate_queryset(queryset, request)
        serializer = self.serializer_class(page, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        request=WarehouseProductSerializer,
        responses={200: WarehouseProductSerializer},
        tags=['Warehouse Product']
    )
    def post(self, request):
        serializer = WarehouseProductSerializer(data=request.data)

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
