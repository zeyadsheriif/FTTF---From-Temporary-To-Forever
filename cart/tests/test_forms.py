from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Product, cart_Custmor, Category
from django.http import HttpRequest
from cart.cart import Cart
from unittest.mock import MagicMock
from django.test import RequestFactory

class CartTestCase(TestCase):

    def setUp(self):
        
        self.category = Category.objects.create(title="Test Category") # Create the category  
        self.product = Product.objects.create(name="Test Product", category=self.category, price=100) # Create the product 
        self.user = User.objects.create_user(username="testuser", password="testpassword") # Create the test user
        

        # Create a mockup session 
        self.request = RequestFactory().get('/')
        self.request.user = self.user
        self.request.session = MagicMock()
        self.cart = Cart(self.request)



    def test_cart_initialization(self): # check that cart starts empty
        self.assertEqual(len(self.cart), 0)

    def test_add_product(self): #test the add to cart funtionality 
        self.cart.add(self.product, 2)
        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart.cart[str(self.product.id)], 2)


    def test_cart_total(self): # test the total cart amout is calculated right
        self.cart.add(self.product, 2)
        total = self.cart.cart_total()
        expected_total = self.product.price * 2
        self.assertEqual(total, expected_total)

    def test_update_product_quantity(self): #test the change in cart when updating
        self.cart.add(self.product, 2)
        self.cart.update(self.product.id, 5)
        self.assertEqual(self.cart.cart[str(self.product.id)], 5)

    def test_delete_product(self): #test the removal of the product from cart when deleting
        self.cart.add(self.product, 2)
        self.cart.delete(self.product.id)
        self.assertEqual(len(self.cart), 0)
    
