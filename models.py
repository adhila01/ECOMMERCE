from django.db import models
from django.db import models

# Create your models here.

class UserRegister(models.Model):
    fullname=models.CharField(max_length=30)
    email=models.CharField(max_length=50)
    phone=models.IntegerField()
    gender=models.CharField(max_length=20)
    propic=models.ImageField(upload_to='images/')
    password=models.CharField(max_length=20)
    def __str__(self):
        return self.fullname

class SellerProductUpload(models.Model):
    productname=models.CharField(max_length=30)
    price=models.IntegerField()
    proimg=models.ImageField(upload_to='images/')
    sizes=models.CharField(max_length=200)
    desc=models.CharField(max_length=200)
    category=models.CharField(max_length=20)
    def __str__(self):
        return self.productname



class CartItem(models.Model):
    userid=models.IntegerField()
    item=models.ForeignKey(SellerProductUpload,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    selectedsize=models.CharField(max_length=20)

class wishlist(models.Model):
    userid=models.IntegerField()
    item=models.ForeignKey(SellerProductUpload,on_delete=models.CASCADE)

class Addressdetails(models.Model):
    userdetails=models.ForeignKey(UserRegister,on_delete=models.CASCADE)
    address_line1=models.CharField(max_length=200)
    address_line2=models.CharField(max_length=200)
    pincode=models.IntegerField()
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    contact_name=models.CharField(max_length=20)
    contact_number=models.IntegerField()

class Order(models.Model):
    userdetails=models.ForeignKey(UserRegister,on_delete=models.CASCADE)
    address=models.ForeignKey(Addressdetails,on_delete=models.CASCADE)
    ordered_date=models.DateTimeField(auto_now_add=True)

class OrderItems(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    order_pic=models.ImageField()
    pro_name=models.CharField(max_length=20)
    quantity=models.IntegerField()
    price=models.IntegerField()
    order_status=models.BooleanField(default=True)

    #here order models have no connection with cart model
# Create your models here.
