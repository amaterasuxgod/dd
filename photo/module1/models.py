from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

class Facility_type(models.Model): 
    title = models.CharField(verbose_name=_("title"), help_text=_("Required"), max_length=255)
    adress = models.CharField(verbose_name=_("adress"), help_text=_("Required"), max_length=255)
    working_places = models.IntegerField()


class Client(models.Model):
    facility = models.ForeignKey(Facility_type, related_name='facilities', on_delete=models.RESTRICT)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    is_professional = models.BooleanField(default=None)
    amount_of_orders = models.IntegerField(default=0)

    def amount_of_orders(self):
        for order in self.clients.all():
            amount_of_orders = amount_of_orders + 1
        
        if amount_of_orders > 10:
            is_professional = True


class Order(models.Model):
    client = models.ForeignKey(Client, related_name='clients', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    urgency_rate = models.IntegerField(default = 3)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def urgency(self):
        if urgency_rate < 2:
            is_urgent = True
            regular_price = regular_price * 2

    def get_total_cost(self):
        return sum(service.get_total_price() for service in self.services.all())


class Services(models.Model):
    order = models.ForeignKey(Order, related_name='services', on_delete=models.RESTRICT)
    title = models.CharField(verbose_name=_("title"), help_text=_("Required"), max_length=255)
    description = models.TextField(verbose_name=_("description"), help_text=_("Not required"), blank=True)
    number_of_photos = models.IntegerField(default=1)
    paper_type = models.CharField(verbose_name=_("title"), help_text=_("Required"), max_length=255)
    photo_format =  models.CharField(verbose_name=_("title"), help_text=_("Required"), max_length=255)
    regular_price = models.FloatField(verbose_name=_("Regular price"), help_text=_("Максимально 10 цифр"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_total_price(self):
        regular_price = regular_price * number_of_photos

                
        if number_of_photos > 20:
            regular_price = regular_price * 0.90


