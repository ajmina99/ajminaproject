from django.contrib import admin
from cart.models import Cart,Order_table,Payment

admin.site.register(Cart)
admin.site.register(Order_table)
admin.site.register(Payment)