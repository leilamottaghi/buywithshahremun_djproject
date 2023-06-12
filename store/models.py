
from django.db import models
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import reverse
# from django_countries.fields import CountryField
import os
from django.core.files import File 
import urllib
import urllib.request
import boto
from boto.s3.key import Key
from urllib.request import urlopen

from io import StringIO,BytesIO
import logging 
import requests
import boto3
from django.contrib.auth import get_user_model
from iranian_cities.models import Province
from iranian_cities.models import County
from iranian_cities.fields import ProvinceField

from django.core.validators import RegexValidator
# Create your models here.


logging.basicConfig(level=logging.INFO)
try:
    s3_resource = boto3.resource(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

except Exception as exc:
    logging.info(exc)



CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)




class Product(models.Model):
    product_link = models.URLField(max_length = 200,validators=
                            [RegexValidator(
                                regex= '/^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/',
                                message='Not a valid URL',
                            )],verbose_name='عنوان')
                            
    weight =models.CharField(max_length=100,default=None,verbose_name='وزن')
    title = models.CharField(max_length=200,verbose_name='عنوان')
    price = models.FloatField(null=True,verbose_name='قیمت اصلی لیر')
    discount_price = models.FloatField(blank=True, null=True,verbose_name='قیمت لیر')
    sizes = models.CharField(max_length=200,default=None,verbose_name='سایز')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2,default=None)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField(verbose_name='توضیحات بیشتر')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


    
 

class Image(models.Model):
    name = models.CharField(blank=True,max_length=20,default='')
    product = models.ForeignKey('Product', on_delete=models.CASCADE,related_name='images')
    image_url = models.CharField(max_length=255,default='https://kavenegar.com/images/verification/header.png')
    image = models.ImageField(upload_to  = 'products/%Y/%m/%d',default=None,blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name





ORDER_STATUS_CHOICES = (
    ('awaiting_payment', 'Awaiting Payment'),
    ('paid', 'Paid'),
    ('ready_to_send', 'Ready to send'),
    ('posted', 'Posted'),
    ('Completed', 'Completed'),
    ('refunded', 'Refunded'),
    ('stale', 'Stale'),
)



class ShippingMethod(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()

    def __str__(self):
        # return self.name
        return f"{self.name}(تومان{self.price}) "


class Order(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, related_name = 'orders')
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='awaiting_payment',verbose_name='وضعیت  سفارش')
    created = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ')
    updated = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=400, default=None,blank=True,verbose_name='یادداشت سفارش')
    address = models.CharField(max_length=400, default=None,blank=True)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True)
    class Meta:
        ordering = ('status','-updated')

    def __str__(self):
        return f'{self.user} - {str(self.id)}'

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_total_quantity(self):
        return sum( item.quantity for item in self.items.all())

    def calculate_total_price(self):
        subtotal = sum( item.get_cost() for item in self.items.all())
        return subtotal + self.shipping_method.price if self.shipping_method else subtotal



class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE , related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity





class Address(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, related_name = 'address',default=None)
    name = models.CharField(max_length=100,default=None,verbose_name='نام')
    last_name = models.CharField(max_length=100,default=None,verbose_name='نام خانوادگی')
    province = models.ForeignKey(Province,on_delete=models.CASCADE, related_name = 'ostan',default=None,verbose_name='استان')
    county = models.ForeignKey(County,on_delete=models.CASCADE, related_name = 'shahrestan',default=None,verbose_name='شهر')
    address_title = models.CharField(max_length=100,default=None,verbose_name=' آدرس عنوان')
    address = models.CharField(max_length=100,verbose_name='آدرس کامل')
    phone_number = models.CharField(max_length=11,default='0',verbose_name='شماره موبایل')
    zip = models.CharField(max_length=100,verbose_name='کد پستی')
    status = models.BooleanField(default=False)
    is_shipping_address = models.BooleanField(default=False)
    def __str__(self):
        return self.address_title

    class Meta:
        verbose_name_plural = 'Addresses'



# class Comment(models.Model):
# 	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='ucomments',default=None)
# 	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ocomments')
# 	reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomments', blank=True, null=True)
# 	is_reply = models.BooleanField(default=False)
# 	body = models.TextField(max_length=400)
# 	created = models.DateTimeField(auto_now_add=True)
    

# 	def __str__(self):
# 		return f'{self.user} - {self.body[:30]}'



class TestModel(models.Model):
    province = ProvinceField()







