from hashlib import sha256
import pytest

import django.test

from core.factories import WalletFactory, TransactionFactory


@pytest.fixture()
def rf() -> django.test.RequestFactory:
    from django.test import RequestFactory

    return RequestFactory()


@pytest.fixture(autouse=True)
def setup_db(db):
    # Create a test wallet
    wallet = WalletFactory()

    # Generate transactions for the wallet
    for i in range(1, 11):
        TransactionFactory(wallet=wallet, amount=i * 2000.0, txid=sha256().hexdigest())
