from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Product, Category, cart_Custmor, order_custmor, rating_custmor
from django.core import mail
import json
from unittest.mock import MagicMock



class CoreViewsTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.client = Client()
        
        # Create test data
        self.category = Category.objects.create(title="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            price=100.00,
            category=self.category,
            description="A test product.",
            stock=5,
            type="Sale",
            rate=4.0,
            rate_count=10,
            image="uploads/product/test_image.jpg" 
        )

        
        self.cart_customer = cart_Custmor.objects.get(user=self.user)
        self.order_customer = order_custmor.objects.get(user=self.user)
        

    # Test for home 
    def test_index_view(self):
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertIn('products', response.context)
        self.assertIn('Categorys', response.context)

    # Test for signup 
    def test_signup_view(self):
        response = self.client.post(reverse('core:signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'cpassword': 'newpassword',
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username='newuser').exists())

    # Test for login 
    def test_userlogin_view(self):
        response = self.client.post(reverse('core:login'), {
            'username': 'testuser',
            'password': 'testpass',
        })
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    # Test for logout 
    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('core:logout'))
        self.assertEqual(response.status_code, 302)  
        self.assertNotIn('_auth_user_id', self.client.session)

    # Test for product detail
    def test_product_detail_view(self):
        response = self.client.get(reverse('core:product_detail', args=[self.product.name]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/productdetail.html')
        self.assertEqual(response.context['product'], self.product)

    # Test for search
    def test_search_view(self):
        response = self.client.get(reverse('core:search_view'), {'q': 'Test Category'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/search.html')
        self.assertTrue(response.context['products'].exists())

    # Test for listcategory 
    def test_listcategory_view(self):
        response = self.client.get(reverse('core:category', args=[self.category.title]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/category.html')
        self.assertIn('products', response.context)

    # Test for rate product 
    def test_rate_product_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('core:rate_product'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_rate': 5,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(rating_custmor.objects.filter(user=self.user, product=self.product).exists())

    # Test for reset pass view
    def test_reset_pass_view(self):
        response = self.client.post(reverse('core:password_reset'), {'email': self.user.email})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)  
