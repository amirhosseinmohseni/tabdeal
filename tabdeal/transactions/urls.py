from django.urls import path
from .views import (
    charge_customer_wallet,
    charge_wallet,
    UserTransferListView,
    UserChargeListView,
    TransferListView,
    ChargeListView,
)

urlpatterns = [
    path("charge-customer-wallet/", charge_customer_wallet, name="charge_customer_wallet"),
    path("charge-wallet/", charge_wallet, name="charge_wallet"),
    path("get_transfers/", UserTransferListView.as_view(), name="get_transfers"),
    path("get_charges/", UserChargeListView.as_view(), name="get_charges"),
    path("all_transfers/", TransferListView.as_view(), name="all_transfers"),
    path("all_charges/", ChargeListView.as_view(), name="all_charges"),
]