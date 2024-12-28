from rest_framework import serializers
from .models import Seller, Customer

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ["phone_number", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return Seller.objects.create_user(**validated_data)
    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["phone_number"]
    
    def create(self, validated_data):
        return Customer.objects.create(**validated_data)