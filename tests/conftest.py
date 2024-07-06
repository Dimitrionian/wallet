from hashlib import sha256
import pytest

from core.factories import WalletFactory, TransactionFactory
from core.models import Wallet


@pytest.fixture(autouse=True)
@pytest.mark.django_db
def setup_db():
    # Create a test wallet
    wallet = WalletFactory()

    # Generate transactions for the wallet
    TransactionFactory(wallet=wallet, txid=sha256())
    TransactionFactory(wallet=wallet, amount=2000.0, txid=sha256().hexdigest())
