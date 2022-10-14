from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings

import uuid
from twilio.rest import Client as TwilioClient
from urllib.parse import urlencode
import phonenumbers
import pycountry

from store.models import Product

# Create your models here.
class Customer(AbstractUser):
  email = models.EmailField(_("email address"), unique=True)
  mobile = models.CharField(max_length=12, unique=True)
  country = CountryField(verbose_name=_("Country"), null=True, blank=True, blank_label='Select country')
  is_active = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  
  two_step_active = models.BooleanField(default=False)
    
  class Meta:
    verbose_name = "Accounts"
    verbose_name_plural = "Accounts"
  
  def __str__(self):
    return f"{self.username}"
  
  def email_user(self, subject, message):
    send_mail(
      subject, message, settings.EMAIL_USERNAME,
      [self.email], fail_silently=False,
    )
  
  def send_sms(self, message):
    country_code = pycountry.countries.get(name = self.country)
    number_object = phonenumbers.parse(self.mobile, country_code).alpha_2
    phone_number = f"+{number_object.country_code}{number_object.national_number}"
    
    
    sid = settings.TWILIO_ACC_SID
    token = settings.TWILIO_AUTH_TOKEN 
    twilio_number = settings.TWILIO_NUMBER 
    
    client = TwilioClient(sid, token)
    
    client.messages.create(
        body=message,
        from_= twilio_number,
        to = self.mobile
      )
  

class Address(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.CASCADE)
  full_name = models.CharField(_("Full Name"), max_length=150)
  phone = models.CharField(_("Phone Number"),max_length=50)
  post_code = models.CharField(_("Postcode"), max_length=12)
  address_line_1 = models.CharField(_("Address Line 1"), max_length=150)
  address_line_2 = models.CharField(_("Address Line 2"), max_length=150, blank=True)
  town_city = models.CharField(_("Town/City/State"), max_length=150)
  country = CountryField(verbose_name=_("Country"), null=True, blank=True)
  delivery_instructions = models.CharField(_("Delivery Instructions"), max_length=250)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  default = models.BooleanField(default=False)
  
  
  class Meta:
    verbose_name = "Address"
    verbose_name_plural = "Addresses"
  
  def __str__(self):
    return f"{self.town_city}"


class UserToken(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  two_step_code = models.CharField(max_length=6, null=True, blank=True)
  is_email = models.BooleanField(default=False)
  is_sms = models.BooleanField(default=False)
  
  is_active = models.BooleanField(default=True)
  
  def __str__(self):
    return f"{self.customer}"