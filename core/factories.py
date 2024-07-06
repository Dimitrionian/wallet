from decimal import Decimal

import factory

from . import models


class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Wallet

    label = 'Wallet #1'


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Transaction

    amount = Decimal('1000.0')

