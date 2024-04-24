from drf_spectacular.utils import extend_schema
from drf_yasg.openapi import Response
from rest_framework import status
from rest_framework.views import APIView

from apps.payment.serializers import PaymentSerializer


class PaymentListView(APIView):

    @extend_schema(
        request=PaymentSerializer,
        responses={201: PaymentSerializer},
        tags=['Payment'],
    )
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
