import datetime
from unicodedata import category
from django.db import models
from django.forms import IntegerField

# Create your models here.


class Registration(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    mobile = models.BigIntegerField()
    gender = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.IntegerField()
    desc = models.CharField(max_length=500)
    pro_image = models.ImageField(upload_to='upload/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class order(models.Model):
    address = models.CharField(max_length=220)
    mobile_no = models.BigIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Registration, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    date = models.DateTimeField(default=datetime.datetime.now())
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product.product_name
