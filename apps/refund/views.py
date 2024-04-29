from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.refund.models import Refund
from apps.refund.serializers import RefundSerializer


class RefundListView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = RefundSerializer

    @extend_schema(
        tags=['Refund'],
        responses={200: serializer_class(many=True)}
    )
    def get(self, request):
        queryset = Refund.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RefundListView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = RefundSerializer

    @extend_schema(
        tags=['Refund'],
        request=serializer_class,
        responses={200: serializer_class}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
