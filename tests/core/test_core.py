import pytest

from core.models import Wallet, Transaction


@pytest.mark.django_db
def test_answer():
    assert Wallet.objects.count() == 1
    assert Transaction.objects.count() == 2

    trs = Transaction.objects.all()
    pass
