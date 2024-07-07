import pytest
from decimal import Decimal
from django.db.models import Sum

from core.models import Wallet, Transaction


@pytest.mark.django_db
def test_balance():
    wallets = Wallet.objects.all()
    balance = sum(wallet.balance for wallet in wallets)
    _balance = Transaction.objects.aggregate(
        amount=Sum("amount", default=Decimal("0.0"))
    )["amount"]
    assert balance == _balance
