import json

from django.conf import settings
from django.urls import reverse
from rest_framework.pagination import LimitOffsetPagination

from api.viewsets import TransactionViewSet, WalletViewSet
from core.models import Transaction, Wallet


def test_paginated_transactions_response(rf):
    transactions = Transaction.objects.count()

    pagination = LimitOffsetPagination()
    queryset = range(0, 10)
    offset = 0
    limit = 10
    count = len(queryset)

    url = f"{settings.TEST_URL.rstrip('/')}{reverse('transactions-list')}"
    request = rf.get(
        url,
        {
            pagination.limit_query_param: limit,
            pagination.offset_query_param: offset,
        },
    )
    response = TransactionViewSet.as_view({"get": "list"})(request)
    content = json.loads(response.rendered_content)
    assert count == content["count"]
    assert transactions == content["count"]


def test_wallets_response(rf):
    wallets = Wallet.objects.all()

    url = f"{settings.TEST_URL.rstrip('/')}{reverse('wallets-list')}"
    request = rf.get(url)
    response = WalletViewSet.as_view({"get": "list"})(request)
    content = json.loads(response.rendered_content)
    assert wallets.count() == content["count"]
