from django.urls import path
from .views import (
    charge_customer_wallet
)

urlpatterns = [
    path("charge-customer-wallet/", charge_customer_wallet, name="charge_customer_wallet"),
]