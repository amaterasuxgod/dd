from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django_countries.fields import CountryField
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils.translation import gettext_lazy as _

class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, email, user_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')
        

        return self.create_user(email, user_name, password, **other_fields)
    
    def create_user(self, email, user_name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email adress'))
        
        email = self.normalize_email(email)

        user = self.model(email=email, user_name=user_name, **other_fields)

        user.set_password(password)

        user.save()
        return user



class Facility_type(models.Model): 
    title = models.CharField(verbose_name=_("title"), help_text=_("Required"), max_length=255)
    adress = models.CharField(verbose_name=_("adress"), help_text=_("Required"), max_length=255)
    working_places = models.IntegerField()


    class Meta:
        verbose_name = 'Филиалы и киоски'
        verbose_name_plural = 'Филиалы и киоски'
    
    def __str__(self):
        return self.title






class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    about = models.TextField(_('about'), max_length=500, blank=True)
    country = CountryField()
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    town_city = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_professional = models.BooleanField(default=False)
    amount_of_orders = models.IntegerField(default=0)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'


    def orders(self):
        self.amount_of_orders = self.amount_of_orders + 1
        
        if self.amount_of_orders > 10:
            self.is_professional = True        

    def __str__(self):
        return self.user_name


class Order(models.Model):
    client = models.ForeignKey(UserBase, related_name='client', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        
    def get_total_cost(self):
            return sum(order.price for order in self.services.all())
    
    def __str__(self):
        return 'Order {}'.format(self.id)



class Services(models.Model):
    title = models.CharField(verbose_name=_("title"), help_text=_("Required"), max_length=255)
    CHOICES = [
        ('good', 'Goods'),
        ('service', 'Services'),
    ]
    category = models.CharField(max_length=32, choices=CHOICES, default='good')
    description = models.TextField(verbose_name=_("Описание"), help_text=_("Not required"), blank=True)
    image = models.ImageField(verbose_name='image', help_text=_("Upload a product image"), default="photos/photo-roll.png", upload_to="photos/")
    regular_price = models.FloatField(verbose_name=_("Regular price"), help_text=_("Максимально 10 цифр"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now_add=True)
    available = models.IntegerField(blank=True, null=True)
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'
    
    
    def __str__(self):
        return self.title

class OrderService(models.Model):
    order = models.ForeignKey(Order, related_name='order', on_delete=models.CASCADE)
    service = models.ForeignKey(Services, related_name='service', on_delete=models.CASCADE)
    urgency_rate = models.IntegerField(null=True)
    facility = models.ForeignKey(Facility_type, related_name='facilities', on_delete=models.RESTRICT, default=None)
    is_urgent = models.BooleanField(default=False)
    number_of_photos = models.IntegerField(default=1)
    paper_type = models.CharField(verbose_name=_("paper type"), help_text=_("Required"), max_length=255, null=True)
    photo_format =  models.CharField(verbose_name=_("photo format"), help_text=_("Required"), max_length=255, null=True)
    price = models.FloatField(verbose_name=_("total price"), help_text=_("Максимально 10 цифр"), default=None)

    class Meta:
        verbose_name = 'Детали заказа'
        verbose_name_plural = 'Детали заказов'
    
    def __str__(self):
        return 'Заказ: {}, срочность: {}'.format(self.order.id,self.urgency_rate)

    def get_total_price(self):


        self.price = self.price * self.number_of_photos

                
        if self.number_of_photos > 20:
            self.price = self.price * 0.90
        

        if self.urgency_rate < 3:
            self.is_urgent = True
            self.price = self.price * 2