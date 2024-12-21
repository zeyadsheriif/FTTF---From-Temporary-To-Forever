import json
from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from core.models import cart_Custmor, Product
from cart.cart import Cart  # Adjust the import path based on your structure

@receiver(user_logged_in)
def sync_cart_on_login(request, user, **kwargs):
    """
    Synchronize the user's cart from the database when they log in.
    """
    if user.is_authenticated:
        cart = Cart(request)  # Initialize the cart object
        current_user = cart_Custmor.objects.filter(user=user).first()

        if current_user and current_user.old_cart:
            saved_cart = current_user.old_cart
            converted_cart = json.loads(saved_cart)  # Convert JSON string to dictionary
            cart.session['session_key'] = {}  # Clear existing session cart
            cart.session.modified = True

            for key, value in converted_cart.items():  # Add products to the session cart
                product = Product.objects.filter(id=key).first()
                if product:
                    cart.add(product=product, quantity=value)
