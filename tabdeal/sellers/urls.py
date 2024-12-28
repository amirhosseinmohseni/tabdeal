from django.urls import path
from .views import (
    RegisterSellerView,
    RegisterCustomerView,
)

urlpatterns = [
    path("register_seller/", RegisterSellerView.as_view(), name="register_seller"),
    path("register_customer/", RegisterCustomerView.as_view(), name="register_customer"),
]