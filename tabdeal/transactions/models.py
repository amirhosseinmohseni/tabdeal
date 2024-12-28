from django.db import models
from sellers.models import Seller, Customer

class Transfer(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='source_seller')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='dest_customer')
    amount = models.PositiveBigIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.created}: {self.seller} transfered {self.amount} to {self.customer}"
    
class Charge(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='charged_seller')
    amount = models.PositiveBigIntegerField()
    is_accept = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.created}: {self.seller} charged {self.amount}"