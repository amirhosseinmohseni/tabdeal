from django.contrib import admin
from .models import Transfer, Charge



class ChargeAdmin(admin.ModelAdmin):
    list_display = ('seller', 'amount', 'is_accept')
    
class TransferAdmin(admin.ModelAdmin):
    list_display = ('seller', 'customer', 'amount')


admin.site.register(Charge, ChargeAdmin)
admin.site.register(Transfer, TransferAdmin)