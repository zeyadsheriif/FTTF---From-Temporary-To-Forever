from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save



class Category(models.Model): #category table is creating containing its title
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Product(models.Model): #product table is created containing it name, price, category, description, image
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0,decimal_places=2, max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    description = models.CharField(max_length=500, default='', blank=True, null=True) 
    stock = models.IntegerField(default='1')
    type = models.CharField(max_length=5,choices=[('Sale', 'sale'), ('Rent', 'rent')], default='Sale')
    image = models.ImageField(upload_to='uploads/product/')
    rate = models.DecimalField(default=0, decimal_places=1, max_digits=10)
    rate_count = models.IntegerField(default=0)
    def __str__(self):
        return self.name


class cart_Custmor(models.Model): #cart per custmor table 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

def create_custmor_cart(sender, instance, created, **kwargs): #auto create a cart for any custmor who is initialized
    if created:
        user_cart_custmor = cart_Custmor(user=instance)
        user_cart_custmor.save()
post_save.connect(create_custmor_cart, sender=User)


class rating_custmor(models.Model): #rating per cutmor
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

class order_custmor(models.Model): #order per custmor
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     phone =  models.IntegerField(default=0, blank=True, null=True)
     address  = models.CharField(max_length=500, default='.', blank=True, null=True) 
     order_items = models.CharField(max_length=200,default='.', blank=True, null=True)
     def __str__(self):
        return self.user.username
def create_custmor_order(sender, instance, created, **kwargs): #auto save user for futue orders
    if created:
        user_order = order_custmor(user=instance)
        user_order.save()
post_save.connect(create_custmor_order, sender=User)



