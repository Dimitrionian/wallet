from rest_framework import serializers

from core.models import Wallet, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=23, decimal_places=18, default=1000.0)

    def validate_amount(self, value):
        """
        Prevent a wallet balance to be negative
        """
        wallet = Wallet.objects.filter(pk=self.context.get("wallet_id")).first()
        if wallet.balance - value < 0:
            raise serializers.ValidationError("Wallet balance cannot be negative")

        return value

    class Meta:
        model = Transaction
        fields = ("id", "wallet", "amount", "txid")


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = (
            "id",
            "label",
            "balance",
        )
