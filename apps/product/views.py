from django.shortcuts import get_object_or_404
from django.db.models import Q 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.product.filters import ProductFilter
from apps.product.models import Product
from apps.product.serializers import ProductSerializer


class ProductListView(APIView, PageNumberPagination):
    permission_classes = (IsAdminUser,)
    serializer_class = ProductSerializer
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

    @extend_schema(
        parameters=[
            OpenApiParameter('page', location=OpenApiParameter.QUERY, type=OpenApiTypes.INT),
            OpenApiParameter('page_size', location=OpenApiParameter.QUERY, type=OpenApiTypes.INT),
            OpenApiParameter('search', location=OpenApiParameter.QUERY, type=OpenApiTypes.STR,
                             description='via name, barcode'),
            OpenApiParameter('currency', location=OpenApiParameter.QUERY, type=OpenApiTypes.STR),
            OpenApiParameter('name', location=OpenApiParameter.QUERY, type=OpenApiTypes.STR),
            OpenApiParameter('barcode', location=OpenApiParameter.QUERY, type=OpenApiTypes.STR),
        ],
        responses={200: serializer_class(many=True)},
        tags=['Product']
    )
    def get(self, request):
        products = Product.objects.all()
        search = request.query_params.get('search', None)
        products = products.filter(Q(name__icontains=search) | Q(barcode__icontains=search)) if search else products

        product_filter = ProductFilter(request.GET, queryset=products)
        queryset = product_filter.qs if product_filter.is_valid() else products.none()
        page = self.paginate_queryset(queryset, request)
        serializer = self.serializer_class(page, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)
    
    @extend_schema(
        request=serializer_class,
        responses={200: serializer_class},
        tags=['Product']
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
    
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
    

class ProductView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = ProductSerializer

    @extend_schema(responses={200: serializer_class},
                   tags=['Product'])
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = self.serializer_class(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(request=serializer_class,
                   responses={200: serializer_class},
                   tags=['Product'])
    def put(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = self.serializer_class(product, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(tags=['Product'])
    def delete(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  
