from dataclasses import dataclass

from django.db import IntegrityError
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, JSONParser

from api.serializers import TransactionSerializer
from core.models import Wallet


@dataclass
class TransactionData:
    transaction_data: dict
    headers: dict
    status: int


class BaseAPIViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    parser_classes = (
        JSONParser,
        MultiPartParser,
    )

    def create_transaction(self, request) -> TransactionData:
        wallet = Wallet.objects.filter(pk=request.data.pop("wallet")).first()
        if wallet is None:
            return TransactionData(
                transaction_data={"success": False, "message": "Wallet does not exist"},
                headers={},
                status=404,
            )

        serializer = TransactionSerializer(
            data=request.data, context={"wallet_id": wallet.id}
        )
        serializer.is_valid(raise_exception=True)

        transaction = self.perform_transaction_create(serializer)
        transaction.wallet = wallet
        transaction.save()

        return TransactionData(
            transaction_data=serializer.data,
            headers=self.get_success_headers(serializer.data),
            status=201,
        )

    def perform_transaction_create(self, serializer):
        try:
            return serializer.save()
        except IntegrityError:
            """
            For that very rare cases when it hasn't been managed to set a unique txid due to sha256 potential non
            unique generations. Client code should retry in this case
            Another possibility is to use a neverending loop but there is a probability of
            the stack overflow error if by some reason the break condition doesn't work
            One more option is to use `for` loop to increase the probability of a successful attempt
            """
            raise ValidationError("Unable to create a transaction, please try again")
