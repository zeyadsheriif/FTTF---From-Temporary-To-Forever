from .cart import Cart

def cart_context(request): # create context processor so that the cart is working in all pages
    return {'cart': Cart(request)} # return default data from the cart