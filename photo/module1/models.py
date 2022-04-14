from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

# Facilities
class Facility_category(MPTTModel):
name = models.CharField(verbose_name=_("Category Name"),help_text=_('Required and unique'),max_length=255,unique=True)
slug = models.SlugField(verbose_name=_("Category safe URL"), max_length=255, unique=True)
parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
is_active = models.BooleanField(default=True)

class MPTTMeta:
order_insertion_by = ["name"]


class Meta:
verbose_name = _("Facility_category")
verbose_name_plural = _("Facility_categories")


def __str__(self):
return self.name

class Facilities(models.Model):
    working_places = models.CharField(verbose_name=_("Working places"),max_length=255)
    adress = models.CharField(verbose_name=_("Adress"),max_length=255)



# User
class Client(models.Model):
is_professional = models.BooleanField(default=False)
discount = models.BooleanField(default=False)





# services
class Services_category(MPTTModel):
name = models.CharField(verbose_name=_("Category Name"),help_text=_('Required and unique'),max_length=255,unique=True)
slug = models.SlugField(verbose_name=_("Category safe URL"), max_length=255, unique=True)
parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
is_active = models.BooleanField(default=True)

class MPTTMeta:
order_insertion_by = ["name"]


class Meta:
verbose_name = _("Services_category")
verbose_name_plural = _("Services_categories")


def __str__(self):
return self.name


class Order(models.Model):
user = models.ForeignKey(Client, on_delete=models.CASCADE)
name = models.CharField(verbose_name=_("Service name"),help_text=_('Required and unique'),max_length=255,unique=True)
price = models.FloatField(verbose_name=_("Price"), help_text=_("Максимально 10 цифр"))
description = models.TextField(verbose_name=_("description"), help_text=_("Not required"), blank=True)
discount = models.CharField(verbose_name=_("discount"))

# goods
class Order_category(MPTTModel):
name = models.CharField(verbose_name=_("Category Name"),help_text=_('Required and unique'),max_length=255,unique=True)
slug = models.SlugField(verbose_name=_("Category safe URL"), max_length=255, unique=True)
parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
is_active = models.BooleanField(default=True)

class MPTTMeta:
order_insertion_by = ["name"]


class Meta:
verbose_name = _("Category")
verbose_name_plural = _("Categories")


def __str__(self):
return self.name

class Goods(models.Model):
category = models.ForeignKey(Goods_category, on_delete=models.RESTRICT)
title = models.CharField(verbose_name=_("title"), help_text=_("Required"), max_length=255)
description = models.TextField(verbose_name=_("description"), help_text=_("Not required"), blank=True)
regular_price = models.FloatField(verbose_name=_("Regular price"), help_text=_("Максимально 10 цифр"))
created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
updated_at = models.DateTimeField(_("Updated at"), auto_now_add=True)


class Meta:
ordering = ("-created_at",)
verbose_name = _("Product")
verbose_name_plural = _("Products")


def __str__(self):
return self.title