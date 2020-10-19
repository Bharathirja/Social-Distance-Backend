from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.core.validators import RegexValidator
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models.signals import post_save
import random
import os
import requests
from django.contrib.auth.hashers import make_password    


class UserManager(BaseUserManager):
   
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('Phone number must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    
    # username = None
    email = models.EmailField('Email',max_length=254, unique=True,null=True)
    # exists = models.BooleanField('exists',default = True,help_text="if true means new user false means exists user")
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.username = self.email
        super(User, self).save(*args, **kwargs)

class EmailOTP(models.Model):
   
    email = models.EmailField(max_length=254, unique=True) 
    otp   = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of OTP sent')
    validated = models.BooleanField(default=False, help_text='If it is true, that means user have validate otp correctly in second API')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField('created_at',auto_now_add=True)
    updated_at = models.DateTimeField('updated_at',auto_now_add=True)

    class Meta:
        verbose_name_plural = "Emails and OTP"
    
    def __str__(self):
        return str(self.email) + ' is sent ' + str(self.otp)

    # def save(self, **kwargs):
    #     some_salt = 'OTP' 
    #     self.otp = make_password(self.otp, some_salt)
       
    #     super(EmailOTP, self).save(**kwargs)

class Common(models.Model):

    created_at = models.DateTimeField('created_at',auto_now_add=True)
    updated_at = models.DateTimeField('updated_at',auto_now_add=True)
    created_user = models.ForeignKey(User,on_delete=models.PROTECT)

    class Meta:
        abstract = True

class VehicleBrand(Common):

    brand_name = models.CharField(max_length=250,unique=True)
    amount = models.IntegerField('amount')
    
    class Meta:
        verbose_name_plural = "Vehicle Brand"

    def __str__(self):
        return str(self.brand_name)

class TimeSlots(Common):

    slot = models.CharField('slot',max_length=250)
    active = models.BooleanField('active',default=True)
    
    class Meta:
        verbose_name_plural = "Time Slots"

    def __str__(self):
        return str(self.slot)

class Area(Common):

    area_name = models.CharField('area_name',max_length=250)

    class Meta:
        verbose_name_plural = "Area"

    def __str__(self):
        return str(self.area_name)


class CustomerProfile(Common):
    
    phone_regex = RegexValidator( regex = r'^\+?1?\d{9,10}$', message ="Phone number must be entered in the format +919999999999. Up to 10 digits allowed.")
    phone       = models.CharField('Phone',validators =[phone_regex], max_length=10)
    name = models.CharField(max_length=250,null=False,blank=False)
    email = models.EmailField(max_length=250, unique = True)
    address = models.CharField(max_length=250)
    photo = models.ImageField(upload_to='customers/', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Customer Profile"

    def __str__(self):
        return "{}".format(self.name)

class Bookings(Common):

    vehicle_type = models.ForeignKey(VehicleBrand,on_delete=models.PROTECT,related_name='vehicle_types')
    slot = models.ForeignKey(TimeSlots, on_delete=models.PROTECT,related_name='time_slot')
    area = models.ForeignKey(Area, on_delete=models.PROTECT,related_name='service_area')
    booking_amount = models.IntegerField('booking_amount',default=0)
    completed = models.BooleanField('completed?',default=False,help_text='If it True means that booking completed. If it False Booking under progress')
    longitude = models.DecimalField('longitude',max_digits=9, decimal_places=6)
    latitude  = models.DecimalField('latitude',max_digits=9, decimal_places=6)
    
    class Meta:
        verbose_name_plural = "Bookings"
        
    def __str__(self):
        return str(self.vehicle_type)

    def save(self, **kwargs):

        if self.completed:
            TimeSlots.objects.filter(slot=self.slot).update(active=True)
        elif self.completed != True:
            TimeSlots.objects.filter(slot=self.slot).update(active=False)

        super(Bookings, self).save(**kwargs)






