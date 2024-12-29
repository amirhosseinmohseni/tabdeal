from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Seller, Customer
from utils.utils import validate_phone_number

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ["phone_number", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return Seller.objects.create_user(**validated_data)
    
    def validate_phone_number(self, phone_number):
        if validate_phone_number(phone_number):
            if Seller.objects.filter(phone_number=phone_number).exists():
                raise serializers.ValidationError("Phone number already exists in sellers")
            if Customer.objects.filter(phone_number=phone_number).exists():
                raise serializers.ValidationError("Phone number already exists in customers")
            else: 
                return phone_number
        else:
            raise serializers.ValidationError("Invalid phone number")
    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["phone_number"]
    
    def create(self, validated_data):
        return Customer.objects.create(**validated_data)
    
    def validate_phone_number(self, phone_number):
        if validate_phone_number(phone_number):
            if Seller.objects.filter(phone_number=phone_number).exists():
                raise serializers.ValidationError("Phone number already exists in sellers")
            if Customer.objects.filter(phone_number=phone_number).exists():
                raise serializers.ValidationError("Phone number already exists in customers")
            else: 
                return phone_number
        else:
            raise serializers.ValidationError("Invalid phone number")
   
class SellerLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, seller):
        token = super().get_token(seller)
        return token