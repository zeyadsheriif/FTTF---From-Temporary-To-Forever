from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . models import Product, Category, cart_Custmor
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
import json
from cart.cart import Cart




def index(request):  
    products = Product.objects.all()  #this gets all products from the database
    Categorys = Category.objects.all() #this gets all categories from the database
    context ={
        'products':products, 
        'Categorys': Categorys
        }
    return render(request, 'core/index.html', context) #the function is passed to the html with all the required data

def contact(request):  

    return render(request, 'core/contact.html') #the function is passed to the html with all the required data

def signup(request):

    if request.method == "POST":  #if a post method is used(required data is submitted) the function gets all the fields
        username = request.POST.get('username')  
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')  

        if password != cpassword: #checks for the password and confirm password are equal
            messages.success(request,"password do not match please try again") #pop a message if does  not match
            return render(request, 'core/signup.html') #redirects to the signup to re signup

        try:
            user = User.objects.create_user(username=username, email=email, password=password) #if password matches create the user
            user.save()
            login(request,user) #log the user in
            messages.success(request,"User created successfully you are in") #pop a message for success login
            return redirect('core:index') #redirect to the home page after login
        except Exception as e:
            return render(request, 'core/signup.html') #if any error happened user is redirected to the sign up to complete the process
             

    return render(request, 'core/signup.html') #when clicking on signup the function direct it to the signup html



def userlogin(request):

    if request.method == "POST": #if a post method is used(required data is submitted) the function gets all the fields
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password) #checks if this user exists in the database

        if user is not None: # if exists
            login(request, user) #userlogin
            current_user = cart_Custmor.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart #get custmors saved cart from the database
            if saved_cart: #check if there is something in the cart
                converted_cart = json.loads(saved_cart) # convert database string into python dictionary
                cart = Cart(request) #get cart 
                for key, value in converted_cart.items():#loop through cart to add products from database
                    cart.db_add(product=key, quantity=value)

            messages.success(request, "you have been logged in ") #pop a message for success login
            return redirect('core:index') #redirect to the home page after login
        else:
            messages.success(request, "no account for this user name please sign up ") #if user does not exist pop message to sign up
            return redirect('core:signup')   #redirected to sign up page


    context = {
        

    }
    return render(request, 'core/login.html',context) #when clicking on login the function direct it to the login html



def logout_view(request): #when clicking on logout the user is logged out
    logout(request)  
    messages.success(request, "you have been logged out ")  #pop a message for logout
    return redirect('core:index') #user is redirected to home page




def product_detail_view(request, name): #when clicking on any specific product 
    product = Product.objects.get(name=name) # the function gets the product
    context = {
    "product": product,
    
    }
    return render(request, "core/productdetail.html", context) # user is directed to the product details page with the product info


def search_view(request): #when searching for a query
    query = request.GET.get("q") # this gets the query
    
    if query:
        products = Product.objects.filter(category__title__icontains=query).order_by("-price") #products are filtered by this query ordered decendingly by price
    else:
        products = Product.objects.none()  #if no product found none is returned

    context = {
        "products": products,  
        "query": query,
    }
    
    return render(request, 'core/search.html', context) #the user is directed to a page for the search results with all the products that matched the query



def listcategory(request, cat): #when clicking on a specific category
    category = Category.objects.get(title=cat) #we get the gategory with this tilte 
    products = Product.objects.filter(category=category) #we get all the products that is in this category
    context={
        "products": products,
        "category": category,
    }
    return render(request, 'core/category.html', context) #the user is directed a pages that conatins all products in this category with its data


def explore(request): #when clicking on explore 
    products = products = Product.objects.all() #we got all products in our database
    context ={
        'products':products, 
        }
    return render(request, 'core/explore.html', context) #the user is directed to a page with all the products 



def rent(request):
    products = Product.objects.filter(type='Rent') #we get all the products that is avaliable for rent
    context={
        "products": products,
    }
    
    return render(request, 'core/rent.html',context)


def reset_pass(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())

            reset_url = f'http://127.0.0.1:8000/reset_password/{uid}/{token}/'

            send_mail(
                'Password Reset Request',
                f'Hello {user.username},\n\nYou can reset your password from this link: {reset_url}',
                'fttfproject@gmail.com',
                [email],
            )
            messages.success(request, "Password reset email has been sent")
            return render(request, 'core/password_reset_form.html')
        except User.DoesNotExist:
            messages.error(request, "No account found for this email. Please sign up.")
            return render(request, 'core/signup.html')
    else:
        return render(request, 'core/password_reset_form.html', {})


def reset_pass_done(request, uidb64, token):
        
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
        username = user.username
        if default_token_generator.check_token(user, token):
            #print(f"UID: {uidb64}, Token: {token}") 
            if request.method == "POST":
                password = request.POST.get('password')
                user.set_password(password)  # Set the new password
                user.save()

                messages.success(request, "Your password has been successfully reset.")
                return render(request, 'core/login.html')# Redirect to the login page after success
            else:
                return render(request, 'core/password_reset_done.html', {'uid': uidb64, 'token': token, 'username':username})
        else:
            messages.error(request, "This password reset link is invalid or has expired.")
            return redirect('core/password_reset')  # Redirect to the password reset page


def contact(request):  

    return render(request, 'core/contact.html') #the function is passed to the html with all the required data

def send_contact(request):
    if request.method == "POST":
        message = request.POST.get('message')
        name = request.POST.get('name')
        email = request.POST.get('email')
        send_mail(
            'Contact regarding FTTF website',
            message,
            email,
            ['fttfproject@gmail.com'],
         )
        send_mail(
            'Contact regarding FTTF website',
            f'Hello {name},\n\n Thanks for contacting us we will consider your email and get back to you shorty....',
            'fttfproject@gmail.com',
            [email],
         )
        messages.success(request, "We have recived your email thanks for your contact")
        return render(request, 'core/contact.html')
    else:
        messages.success(request, "Unexpected error happened please try again..")
        return render(request, 'core/contact.html')
        

