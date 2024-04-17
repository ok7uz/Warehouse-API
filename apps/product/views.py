from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.product.filters import ProductFilter
from apps.product.models import WarehouseProduct, Product
from apps.product.serializers import WarehouseProductSerializer, ProductSerializer


class ProductListView(APIView, PageNumberPagination):
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('currency', openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
        responses={200: serializer_class},
        tags=['Product']
    )
    def get(self, request):
        products = Product.objects.all()
        filter = ProductFilter(request.GET, queryset=products)
        queryset = filter.qs if filter.is_valid() else products.none()
        page = self.paginate_queryset(queryset, request)
        serializer = self.serializer_class(page, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)
    
    # @swagger_auto_schema(
    #     request_body=serializer_class,
    #     responses={200: serializer_class},
    #     tags=['Product']
    # )
    # def post(self, request, format=None):
    #     serializer = self.serializer_class(data=request.data)
    #
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_paginated_response(self, data):

        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'data': data,
        })
    

class ProductView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer

    @swagger_auto_schema(responses={200: serializer_class},
                         tags=['Product'])
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = self.serializer_class(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=serializer_class,
                         responses={200: serializer_class},
                         tags=['Product'])
    def put(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = self.serializer_class(product, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(tags=['Product'])
    def delete(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  


class WarehouseProductListView(APIView):
    @swagger_auto_schema(
        responses={200: WarehouseProductSerializer(many=True)},
        tags=['Warehouse Product']
    )
    def get(self, request):
        queryset = WarehouseProduct.objects.all()
        serializer = WarehouseProductSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=WarehouseProductSerializer(),
        responses={200: WarehouseProductSerializer()},
        tags=['Warehouse Product']
    )
    def post(self, request, format=None):
        serializer = WarehouseProductSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
