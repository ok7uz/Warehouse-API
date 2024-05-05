from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.cash.models import Cash, Cashier, Sale
from apps.cash.serializers import CashSerializer, CashierSerializer, SaleSerializer


class SaleList(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SaleSerializer

    @extend_schema(
        tags=['Sale'],
        responses={200: SaleSerializer(many=True)}
    )
    def get(self, request):
        sales = Sale.objects.all()
        serailizer = SaleSerializer(sales, many=True)
        return Response(serailizer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        tags=['Sale'],
        request=SaleSerializer,
        responses={200: SaleSerializer(many=True)}
    )
    def post(self, request):
        serializer = SaleSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaleDetail(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SaleSerializer

    @extend_schema(responses={200: serializer_class},
                   tags=['Sale'])
    def get(self, request, sale_id):
        sale = get_object_or_404(Sale, id=sale_id)
        serializer = self.serializer_class(sale, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(request=serializer_class,
                   responses={200: serializer_class},
                   tags=['Product'])
    def put(self, request, sale_id):
        sale = get_object_or_404(Sale, id=sale_id)
        serializer = self.serializer_class(sale, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(tags=['Product'])
    def delete(self, request, sale_id):
        sale = get_object_or_404(Sale, id=sale_id)
        sale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  



class CashierList(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CashierSerializer

    @extend_schema(
        tags=['Cashier'],
        responses={200: CashierSerializer(many=True)}
    )
    def get(self, request):
        cashiers = Cashier.objects.all()
        serailizer = CashierSerializer(cashiers, many=True)
        return Response(serailizer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        tags=['Cashier'],
        request=CashierSerializer,
        responses={200: CashierSerializer(many=True)}
    )
    def post(self, request):
        serializer = CashierSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CashList(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CashSerializer

    @extend_schema(
        tags=['Cash'],
        responses={200: CashSerializer(many=True)}
    )
    def get(self, request):
        cashs = Cash.objects.all()
        serailizer = CashSerializer(cashs, many=True)
        return Response(serailizer.data, status=status.HTTP_200_OK)
