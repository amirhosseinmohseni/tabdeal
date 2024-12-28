from django.urls import path, include

urlpatterns = [
    path('users/', include('sellers.urls')),
    path('transactions/', include('transactions.urls')),
]