from distutils.command.upload import upload
from email.mime import image
from itertools import product
from operator import mod, truediv
from pyexpat import model
from re import L, M
from django.utils import timezone
from tkinter.messagebox import NO
from unicodedata import name
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.


class Categories(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Color(models.Model):
    name=models.CharField(max_length=30)
    code=models.CharField(max_length=30)

    def __str__(self):
        return self.name


class FilterPrice(models.Model):
    FILTERPRICE=(
        ('100 To 1000','100 To 1000'),
        ('1000 To 5000','1000 To 5000'),
        ('5000 To 10000','5000 To 10000'),
        ('10000 To 30000','10000 To 30000'),
        ('30000 To 100000','30000 To 100000'),
        ('100000 & Above','100000 & Above'),
    )

    price=models.CharField(choices=FILTERPRICE,max_length=30)

    def __str__(self):
        return self.price


class Product(models.Model):
    CONDITION=(
        ('New','New'),
        ('Old','Old'),
    )

    STOCK=(
        ('IN STOCK','IN STOCK'),
        ('OUT OF STOCK','OUT OF STOCK'),
    )

    STATUS=(
        ('Publish','Publish'),
        ('Draft','Draft')
    )

    unique_id=models.CharField(max_length=100,unique=True,null=True,blank=True)
    image=models.ImageField(upload_to='store/images/product')
    name=models.CharField(max_length=250)
    price=models.IntegerField()
    condition=models.CharField(choices=CONDITION,max_length=25)
    information=RichTextField(null=True)
    description=RichTextField(null=True)
    stock=models.CharField(choices=STOCK,max_length=25)
    status=models.CharField(choices=STATUS,max_length=25)
    created_date=models.DateTimeField(default=timezone.now,max_length=25)

    categories=models.ForeignKey(Categories,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    filter_price=models.ForeignKey(FilterPrice,on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        if self.unique_id is None and self.created_date and self.id:
            self.unique_id=self.created_date.strftime('75%Y%m%d23') + str(self.id)
        return super().save(*args,**kwargs)

    def __str__(self):
        return self.name


class Images(models.Model):
    image=models.ImageField(upload_to='store/images/product')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)



class Tag(models.Model):
    name=models.CharField(max_length=100)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)



class ContactUs(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    subject=models.CharField(max_length=200)
    message=models.TextField()
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    address=models.TextField()
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    postcode=models.IntegerField()
    phone=models.IntegerField()
    email=models.EmailField()
    amount=models.CharField(max_length=20)
    payment_id=models.CharField(max_length=100,null=True,blank=True)
    paid=models.BooleanField(default=False,null=True)
    date=models.DateField(auto_now_add=True)


    def __str__(self):
        return self.user.username


class OrderItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.CharField(max_length=250)
    image=models.ImageField(upload_to='store/images/order')
    quantity=models.CharField(max_length=20)
    price=models.CharField(max_length=20)
    total=models.CharField(max_length=100)


    def __str__(self):
        return self.order.user.username