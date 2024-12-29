from django.db import transaction as db_transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from sellers.models import Seller, Customer
from .models import Transfer, Charge
from .serializers import TransferRequestSerializer, TransferResponseSerializer, ChargeRequestSerializer, ChargeResponseSerializer, GetTransfersSerializer


executor = ThreadPoolExecutor(max_workers=4)

def process_transfer(seller: Seller, customer_phone_number: str, amount: int):
    try:
        if amount <= 0:
            raise ValueError("Invalid amount.")
        with db_transaction.atomic():
            seller = Seller.objects.select_for_update().get(id=seller.id)
            customer = Customer.objects.select_for_update().get(phone_number=customer_phone_number)

            if seller.wallet < amount:
                raise ValueError("Insufficient balance.")

            seller.wallet -= amount
            customer.wallet += amount

            seller.save()
            customer.save()

            return {
                "status": "success", 
                "message": f"Transferred {amount} from Seller {seller} to Customer {customer}",
                "seller": seller,
                "customer": customer,
                "amount": amount,
                "created": datetime.now()
            }
    except Customer.DoesNotExist:
        return {"status": "error", "message": "Customer not found."}
    except ValueError as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": "An unexpected error occurred."}

@extend_schema(
    request=TransferRequestSerializer,
    responses=TransferResponseSerializer
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def charge_customer_wallet(request):
    try:
        seller = request.user
        serializer = TransferRequestSerializer(data=request.data)
        if serializer.is_valid():
            
            customer_phone_number = serializer.validated_data["phone_number"]
            amount = serializer.validated_data["amount"]

            future = executor.submit(process_transfer, seller, customer_phone_number, amount)
            result = future.result()
            response = TransferResponseSerializer(result)
            
            if result["status"] == "success":
                return Response(
                    response.data, 
                    status=status.HTTP_201_CREATED
                )
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    request=ChargeRequestSerializer,
    responses=ChargeResponseSerializer
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def charge_wallet(request):
    try:
        seller = request.user
        serializer = ChargeRequestSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data["amount"]

            if not amount or amount <= 0:
                return Response({"error": "Invalid amount"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            Charge.objects.create(
                seller=seller,
                amount=amount,
                is_accept=False,
            )
            
            response = ChargeResponseSerializer(data={
                    "seller": seller.id,
                    "amount": amount,
                    "created": datetime.now(),
                    "is_accept": False,
            })
            if response.is_valid():
                return Response(
                    response.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(response.errors, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    responses=TransferResponseSerializer(many=True)
)
class UserTransferListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            seller = request.user
            transfers = Transfer.objects.filter(seller_id=seller.id)
            serializer = TransferResponseSerializer(transfers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@extend_schema(
    responses=ChargeResponseSerializer(many=True)
)
class UserChargeListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            seller = request.user
            charges = Charge.objects.filter(seller_id=seller.id)
            serializer = ChargeResponseSerializer(charges, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@extend_schema(
    responses=TransferResponseSerializer(many=True)
)
class TransferListView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        try:
            transfers = Transfer.objects.all()
            serializer = TransferResponseSerializer(transfers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@extend_schema(
    responses=ChargeResponseSerializer(many=True)
)
class ChargeListView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        try:
            charges = Charge.objects.all()
            serializer = ChargeResponseSerializer(charges, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)