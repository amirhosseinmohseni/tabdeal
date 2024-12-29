from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Charge
from sellers.models import Seller
from logs.utils import write_log

@receiver(post_save, sender=Charge)
def on_charge_accept(sender, instance, created, **kwargs):
    if not created and instance.is_accept:
        seller = Seller.objects.select_for_update().get(id=instance.seller_id)
        seller.wallet += instance.amount
        seller.save()
        write_log(level="INFO", 
                    message=f"Seller wallet charged successfully.", 
                    type="Charge",
                    source=seller,
                    destination=seller,
                    amount=seller,
                    accept=True
        )
        print(f"Account {instance.seller_id} has been charged {instance.amount}!")