from django.contrib import admin
from .models import Product, Category, cart_Custmor, rating_custmor,order_custmor
from django.contrib.auth.models import User



admin.site.register(Product)
admin.site.register (Category)
admin.site.register(cart_Custmor)
admin.site.register(rating_custmor)
admin.site.register(order_custmor)


class cart_Custmorinline(admin.StackedInline):
    model = cart_Custmor

class useradmin(admin.ModelAdmin):  
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [cart_Custmorinline]

admin.site.unregister(User)
admin.site.register(User,useradmin)
