from django.contrib import admin
from .models import Facility_type, Client, Order, Services

# Register your models here.
admin.site.register(Facility_type)
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Services)