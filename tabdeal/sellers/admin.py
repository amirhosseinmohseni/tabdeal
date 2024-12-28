from django.contrib import admin
from .models import Seller, Customer

class SellerAdmin(admin.ModelAdmin):
	list_display = ('phone_number', 'active', 'wallet')

	def active(self, obj):
		return obj.is_active == 1

	active.boolean = True
 
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'wallet')


admin.site.register(Seller, SellerAdmin)
admin.site.register(Customer, CustomerAdmin)