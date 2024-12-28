from django.urls import path
from .views import (
    RegisterSellerView,
    RegisterCustomerView,
    SellerLoginView
)

urlpatterns = [
    path("register_seller/", RegisterSellerView.as_view(), name="register_seller"),
    path("register_customer/", RegisterCustomerView.as_view(), name="register_customer"),
    path("login_seller/", SellerLoginView.as_view(), name="login_seller"),
]