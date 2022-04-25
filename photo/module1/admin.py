from django.contrib import admin
from .models import Facility_type, UserBase, Order, Services, OrderService

# Register your models here.
admin.site.register(Facility_type)
admin.site.register(UserBase)
admin.site.register(Order)
admin.site.register(Services)
admin.site.register(OrderService)