from django.db import transaction as db_transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from sellers.models import Seller, Customer
from .models import Transfer, Charge
from .serializers import TransferRequestSerializer, TransferResponseSerializer, ChargeRequestSerializer, ChargeResponseSerializer, GetTransfersSerializer


@extend_schema(
    request=TransferRequestSerializer,
    responses=TransferResponseSerializer
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def charge_customer_wallet(request):
    seller = request.user
    customer_phone_number = request.data.get("phone_number")
    amount = request.data.get("amount", 0)

    if amount <= 0:
        return Response({"error": "Invalid amount"}, status=400)

    try:
        with db_transaction.atomic():
            seller_wallet = seller.wallet
            customer = Customer.objects.select_for_update().get(phone_number=customer_phone_number)

            if seller_wallet < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            seller.wallet -= amount
            customer.wallet += amount

            seller.save()
            customer.save()

            Transfer.objects.create(
                seller=seller,
                customer=customer,
                amount=amount,
            )
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)

    return Response({
        "seller": seller.id,
        "customer": customer.id,
        "amount": amount,
        "created": datetime.now()
    })

@extend_schema(
    request=ChargeRequestSerializer,
    responses=ChargeResponseSerializer
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def charge_wallet(request):
    seller = request.user
    amount = request.data.get("amount")

    if not amount or amount <= 0:
        return Response({"error": "Invalid amount"}, status=400)

    Charge.objects.create(
        seller=seller,
        amount=amount,
        is_accept=False,
    )
    return Response({
        "seller": seller.id,
        "amount": amount,
        "created": datetime.now(),
        "is_accept": False,
    })

@extend_schema(
    responses=TransferResponseSerializer(many=True)
)
class UserTransferListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        seller = request.user
        transfers = Transfer.objects.filter(seller_id=seller.id)
        serializer = TransferResponseSerializer(transfers, many=True)
        return Response(serializer.data)
    
@extend_schema(
    responses=ChargeResponseSerializer(many=True)
)
class UserChargeListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        seller = request.user
        charges = Charge.objects.filter(seller_id=seller.id)
        serializer = ChargeResponseSerializer(charges, many=True)
        return Response(serializer.data)
    
@extend_schema(
    responses=TransferResponseSerializer(many=True)
)
class TransferListView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        transfers = Transfer.objects.all()
        serializer = TransferResponseSerializer(transfers, many=True)
        return Response(serializer.data)
    
@extend_schema(
    responses=ChargeResponseSerializer(many=True)
)
class ChargeListView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        charges = Charge.objects.all()
        serializer = ChargeResponseSerializer(charges, many=True)
        return Response(serializer.data)