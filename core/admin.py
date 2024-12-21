from django.contrib import admin
from .models import Product, Category, cart_Custmor
from django.contrib.auth.models import User


#tables are registered to the database
admin.site.register(Product)
admin.site.register (Category)
admin.site.register(cart_Custmor)
# admin.site.register(Vendor)
# admin.site.register (CartOrder)
# admin.site.register (CartOrderItems)
# admin.site.register (ProductReview)
# admin.site.register (wishlist)
# admin.site.register(Address)
# admin.site.register(discounts)

class cart_Custmorinline(admin.StackedInline):
    model = cart_Custmor

class useradmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [cart_Custmorinline]

admin.site.unregister(User)
admin.site.register(User,useradmin)
