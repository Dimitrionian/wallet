from hashlib import sha256
import pytest
from decimal import Decimal

import django.test

from core.factories import WalletFactory, TransactionFactory


@pytest.fixture()
def rf() -> django.test.RequestFactory:
    from django.test import RequestFactory

    return RequestFactory()


@pytest.fixture(autouse=True)
def setup_db(db):
    # Create a test wallet #1
    wallet = WalletFactory()

    # Generate transactions for the wallet
    for i in range(1, 6):
        TransactionFactory(
            wallet=wallet, amount=Decimal(i * 2000.0), txid=sha256().hexdigest()
        )

    # Create a test wallet #2
    _wallet = WalletFactory(label="Wallet #2")

    # Generate transactions for the wallet
    for i in range(6, 11):
        TransactionFactory(
            wallet=_wallet, amount=Decimal(i * 2000.0), txid=sha256().hexdigest()
        )
