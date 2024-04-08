from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from apps.product.models import Inventory, Product
from apps.product.serialzers import InventorySerializer, ProductSerializer


class ProductListView(APIView):
    @swagger_auto_schema(
        responses={200: ProductSerializer(many=True)},
        tags=['Product']
    )
    def get(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=ProductSerializer(),
        responses={200: ProductSerializer()},
        tags=['Product']
    )
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductView(APIView):
    @swagger_auto_schema(
        responses={200: ProductSerializer()},
        tags=['Product']
    )
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=ProductSerializer(),
        responses={200: ProductSerializer()},
        tags=['Product']
    )
    def put(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        tags=['Product']
    )
    def delete(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  


class InventoryListView(APIView):
    @swagger_auto_schema(
        responses={200: InventorySerializer(many=True)},
        tags=['Inventory']
    )
    def get(self, request):
        queryset = Inventory.objects.all()
        serializer = InventorySerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=InventorySerializer(),
        responses={200: InventorySerializer()},
        tags=['Inventory']
    )
    def post(self, request, format=None):
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class InventoryView(APIView):
    @swagger_auto_schema(
        responses={200: InventorySerializer()},
        tags=['Inventory']
    )
    def get(self, request, inventory_id):
        inventory = get_object_or_404(Inventory, id=inventory_id)
        serializer = InventorySerializer(inventory, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=InventorySerializer(),
        responses={200: InventorySerializer()},
        tags=['Inventory']
    )
    def put(self, request, inventory_id):
        inventory = get_object_or_404(Inventory, id=inventory_id)
        serializer = InventorySerializer(inventory, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        tags=['Inventory']
    )
    def delete(self, request, inventory_id):
        inventory = get_object_or_404(Inventory, id=inventory_id)
        inventory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  
