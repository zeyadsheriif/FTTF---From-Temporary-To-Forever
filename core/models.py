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
    stock = models.IntegerField(max_length=500, default='1')
    type = models.CharField(max_length=5,choices=[('Sale', 'sale'), ('Rent', 'rent')], default='Sale')
    image = models.ImageField(upload_to='uploads/product/')
    def __str__(self):
        return self.name


class cart_Custmor(models.Model): #custmor table is created containging its email, username, password
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

def create_custmor_cart(sender, instance, created, **kwargs):
    if created:
        user_cart_custmor = cart_Custmor(user=instance)
        user_cart_custmor.save()
post_save.connect(create_custmor_cart, sender=User)

# class discounts(models.Model): #discounts table is created containing its product, discount amount, and new price
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
#     disamount = models.CharField(max_length=100)
#     newprice = models.DecimalField(default=0,decimal_places=2, max_digits=10)

# STATUS_CHOICE = (
#     ("process", "Processing"),
#     ("shipped", "Shipped"),
#     ("delivered", "Delivered"),
# )

# class CartOrder(models.Model): #cart order table is created containing its user, product price, paid status, order date, and product status
#     user = models.ForeignKey(Custmor, on_delete=models.CASCADE)
#     price = models.ForeignKey(Product, on_delete=models.CASCADE)
#     paid_status = models.BooleanField(default=False)
#     order_date = models.DateTimeField(auto_now_add=True)
#     product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="process")



# class CartOrderItems(models.Model): #cart order items table is created containing its order, invoice number, product status, item, quantity, price, and total
#     order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
#     invoice_no = models.CharField(max_length=200)
#     product_status = models.CharField(max_length=200)
#     item = models.CharField(max_length=200)
#     qty = models.IntegerField(default=0)
#     price = models.ForeignKey(Product, on_delete=models.CASCADE)
#     total = models.DecimalField(max_digits=12, decimal_places=2, default="1.99")

# RATING = (
#     (1, "★☆☆☆☆"),
#     (2, "★★☆☆☆"),
#     (3, "★★★☆☆"),
#     (4, "★★★★☆"),
#     (5, "★★★★★"),
# )

# class ProductReview(models.Model): #product review table is created containing its user, product, review text, rating, and date
#     user = models.ForeignKey(Custmor, on_delete=models.CASCADE, null=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
#     review = models.TextField()
#     rating = models.IntegerField(choices=RATING, default=None)
#     date = models.DateTimeField(auto_now_add=True)




# class wishlist(models.Model): #wishlist table is created containing its user, product, and date
#     user = models.ForeignKey(Custmor, on_delete=models.SET_NULL, null=True)
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     date = models.DateTimeField(auto_now_add=True)

# class Address(models.Model): #address table is created containing its user and address
#     user = models.ForeignKey(Custmor, on_delete=models.SET_NULL, null=True)
#     address = models.CharField(max_length=100, null=True)

# class Vendor(models.Model): #vendor table is created containing its username, contact, address, and description
#     username = models.CharField(max_length=100, unique=True)
#     contact = models.CharField(max_length=100, default='')
#     address = models.CharField(max_length=100, default="")
#     description = models.TextField(null=True, blank=True, default="")
#     def _str_(self):
#         return self.name

    