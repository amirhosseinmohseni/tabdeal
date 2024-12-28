from rest_framework import serializers

from .models import Transfer, Charge


class TransferRequestSerializer(serializers.Serializer):
    """Serializer for transfer request data."""
    phone_number = serializers.CharField(max_length=11)
    amount = serializers.IntegerField(min_value=0)

class TransferResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('seller','customer', 'amount', 'created')
        
class ChargeRequestSerializer(serializers.Serializer):
    """Serializer for charge request data."""
    amount = serializers.IntegerField(min_value=0)
    
class ChargeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = ('seller', 'amount', 'created', 'is_accept')
        
class GetTransfersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('seller', 'customer', 'amount', 'created')