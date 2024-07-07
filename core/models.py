from decimal import Decimal
from hashlib import sha256

from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string


class Wallet(models.Model):
    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    label = models.CharField(
        max_length=16,
        verbose_name=_("Label"),
        help_text=_("The wallet label"),
    )

    @property
    def balance(self) -> Decimal:
        """Calculate balance as sum of the wallet transactions"""

        return self.transactions.aggregate(amount=Sum("amount", default=Decimal("0.0")))["amount"]

    def __str__(self) -> str:
        return f"{self.label}"


class Transaction(models.Model):
    wallet = models.ForeignKey(
        "Wallet",
        verbose_name=_("Wallet"),
        help_text=_("The transaction wallet"),
        on_delete=models.CASCADE,
        related_name="transactions",
        null=True,
        blank=True
    )

    _txid = models.CharField(
        max_length=64,
        unique=True,
        verbose_name=_("TXID"),
        help_text=_("Transaction id"),
    )

    @property
    def txid(self):
        return self._txid

    @txid.setter
    def txid(self, value: str):
        self._txid = value

    amount = models.DecimalField(
        max_digits=23,
        decimal_places=18,
        default=0,
        verbose_name=_("Amount"),
        help_text=_("Transaction amount"),
    )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.txid = sha256(get_random_string(64).encode('utf-8')).hexdigest()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self) -> str:
        return f"{self.amount} - {self.txid[:4]}..."
