from django.db import transaction as db_transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sellers.models import Seller, Customer
from .models import Transfer, Charge

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

    return Response({"message": "Transfer successful"})