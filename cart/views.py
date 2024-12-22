from django.shortcuts import render, get_object_or_404
from.cart import Cart
from core.models import Product
from django.http import JsonResponse
from django.contrib import messages




def cart_summary(request): #for the cart summary page with all the products
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    context = {
        'cart_products':cart_products,
        'quantity': quantities,
        'totals' : totals,

    }
    return render(request, "core/cartsummary.html",context)

def cart_add(request): #adds the cart products
    cart = Cart(request) #get the cart
    
    if request.POST.get('action') == 'post': #check for post action
        if request.user.is_authenticated: 
            product_id = int(request.POST.get('product_id')) #gets product id from the frontend
            Product_qty = int(request.POST.get('product_qty'))
            product = get_object_or_404(Product, id= product_id) #lookup product from the database
            if product.stock >= Product_qty: #check that the amount doesnot exceed the stock
                cart.add(product=product, quantity=Product_qty) #save to session
                cart_quantity = cart.__len__()
                response = JsonResponse({'qty': cart_quantity})
                messages.success(request, "product added to cart successfully ") 
                return response
            else:
                messages.success(request, "There is no enough stock for this quantity please try again.... ")
                return JsonResponse({'error': ''}, status=402)
        else:
            messages.success(request, "please login to be able to add to cart ")
            return JsonResponse({'error': ''}, status=401)


def cart_update(request): #update the cart products
    cart = Cart(request)
    if request.POST.get('action') == 'post': #check for post action
       product_id = int(request.POST.get('product_id')) #gets product id from the frontend
       Product_qty = int(request.POST.get('product_qty'))
       product = get_object_or_404(Product, id= product_id) #lookup products in db
       if product.stock >= Product_qty: #check that the amount doesnot exceed the stock
         cart.update(product=product_id, quantity=Product_qty)
         response = JsonResponse({'qty': Product_qty})
         messages.success(request, "product updated successfully ") 
         return response
       else: 
         messages.success(request, "There is no enough stock for this quantity please try again.... ")
         return JsonResponse({'error': ''}, status=402)

       


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post': #check for post action
       product_id = int(request.POST.get('product_id')) #gets product id from the frontend
       cart.delete(product=product_id)
       response = JsonResponse({'product': product_id})
       messages.success(request, "product deleted successfully ") 
       return response