from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

from .serializers import SellerSerializer, CustomerSerializer, SellerLoginSerializer


class RegisterSellerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SellerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Seller registered successfully"}, status=status.HTTP_201_CREATED)
    
class RegisterCustomerView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Customer registered successfully"}, status=status.HTTP_201_CREATED)
    
class SellerLoginView(TokenObtainPairView):
    serializer_class = SellerLoginSerializer