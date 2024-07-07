from rest_framework import mixins
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from api.base import BaseAPIViewSet
from api.serializers import WalletSerializer, TransactionSerializer
from core.models import Wallet, Transaction


class WalletViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    BaseAPIViewSet,
):
    queryset = Wallet.objects.all().order_by("label")
    serializer_class = WalletSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]
    filterset_fields = ["id", "label"]

    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=WalletSerializer, description="Create a wallet"
            ),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class TransactionViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    BaseAPIViewSet,
):
    queryset = Transaction.objects.select_related("wallet").order_by("amount")
    serializer_class = TransactionSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]
    filterset_fields = ["wallet__id", "_txid"]

    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=TransactionSerializer, description="Create a transaction"
            ),
        }
    )
    def create(self, request, *args, **kwargs):
        data = self.create_transaction(request)
        return Response(data.transaction_data, status=data.status, headers=data.headers)
