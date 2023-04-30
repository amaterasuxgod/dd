from django.contrib import admin
from .models import Facility_type, UserBase, Order, Services, OrderService, Order_photo,UserOrderHistory

# Register your models here.
admin.site.register(Facility_type)
admin.site.register(UserBase)
admin.site.register(Order)
admin.site.register(Services)
admin.site.register(OrderService)
admin.site.register(Order_photo)
admin.site.register(UserOrderHistory)