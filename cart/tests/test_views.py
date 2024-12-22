from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Product, Category, cart_Custmor
from ..cart import Cart
from django.contrib.messages import get_messages
from unittest.mock import patch




class CartViewsTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpassword') #create user
        self.category = Category.objects.create(title="Test Category") #create category
        

        self.product = Product.objects.create(   #create product 
            name="Test Product",
            price=100.00,
            category=self.category,
            description="A test product.",
            stock = 10,  
            type="Sale",
            rate=4.0,
            rate_count=10
        )
        
        self.cart_url = reverse('cart:cart_summary')  # initialize the reverse of the cart

    def test_cart_summary_view(self):  #check the viewing of cart summary page
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/cartsummary.html')

        
    @patch('cart.cart.Cart.add')  #test adding to cart with logging in 
    def test_cart_add_view_authenticated(self, mock_add):
        self.client.login(username='testuser', password='testpassword') #log a user in
        data = {  #create the data that is sent from the front
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 2
        }
        response = self.client.post(reverse('cart:cart_add'), data) #recives the data
        mock_add.assert_called_once_with(product=self.product, quantity=2) #check the add function calling
        
        self.assertEqual(response.status_code, 200) #check for success respone 
        self.assertContains(response, 'qty') #check the quantity in respone
        messages = list(get_messages(response.wsgi_request)) #gets the messages from http respone 
        self.assertEqual(str(messages[0]), 'product added to cart successfully ')



    
    def test_cart_add_view_not_authenticated(self): #test adding to cart without login 

        data = { #create the data that is sent from the front
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 2
        }
        response = self.client.post(reverse('cart:cart_add'), data) #recives the data
        
        self.assertEqual(response.status_code, 401) #check for success respone 
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'please login to be able to add to cart ')



    
def test_cart_add_view_insufficient_stock(self): #check adding to cart amout exceding the stock
    self.client.login(username='testuser', password='testpassword')

    data = {
        'action': 'post',
        'product_id': self.product.id,
        'product_qty': 20  
    }
    response = self.client.post(reverse('cart:cart_add'), data)

    self.assertEqual(response.status_code, 402, msg=f"Expected 402 but got {response.status_code}")
    messages = list(get_messages(response.wsgi_request))
    self.assertIn('There is not enough stock', str(messages[0]))




    def test_cart_update_view_authenticated(self): #test cart updating quantity 
        self.client.login(username='testuser', password='testpassword')
        self.client.post(reverse('cart:cart_add'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 2
        })
        
        data = {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 5
        }
        
        response = self.client.post(reverse('cart:cart_update'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'qty')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'product updated successfully ')
        
    
    def test_cart_update_view_insufficient_stock(self): #test updating amout exceding the stock
        self.client.login(username='testuser', password='testpassword')
        self.client.post(reverse('cart:cart_add'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 2
        })
        
        data = {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 20 
        }
        
        response = self.client.post(reverse('cart:cart_update'), data)
        print(f'product{self.product.id} name {self.product.name} stock {self.product.stock} {data}')
        self.assertEqual(response.status_code, 402)
        print(f'the error{respone.status_code}')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'There is no enough stock for this quantity please try again.... ')



    def test_cart_delete_view_authenticated(self): #test deleting from cart
        self.client.login(username='testuser', password='testpassword')
        self.client.post(reverse('cart:cart_add'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 2
        })
        
        data = {
            'action': 'post',
            'product_id': self.product.id
        }
        
        response = self.client.post(reverse('cart:cart_delete'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'product')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'product deleted successfully ')
