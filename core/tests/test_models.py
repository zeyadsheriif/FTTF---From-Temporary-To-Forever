from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Category, Product, cart_Custmor, rating_custmor, order_custmor

class CategoryModelTestCase(TestCase):  #test categry retrival
    def setUp(self):
        self.category = Category.objects.create(title="Test Category")

    def test_str_representation(self):
        self.assertEqual(str(self.category), "Test Category")

class ProductModelTestCase(TestCase): #test the product retrival
    def setUp(self): #create data for product
        self.category = Category.objects.create(title="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            price=100.00,
            category=self.category,
            description="This is a test product.",
            stock=10,
            type="Sale",
            rate=4.5,
            rate_count=5,
            image="uploads/product/test_image.jpg" 
        )

    def test_str_representation(self):
        self.assertEqual(str(self.product), "Test Product")

    def test_product_fields(self):
        self.assertEqual(self.product.price, 100.00)
        self.assertEqual(self.product.stock, 10)
        self.assertEqual(self.product.type, "Sale")
        self.assertEqual(self.product.category, self.category)



class CartCustomerModelTestCase(TestCase): #check cart per user retrival
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.cart_customer = cart_Custmor.objects.get(user=self.user)

    def test_str_representation(self):
        self.assertEqual(str(self.cart_customer), "testuser")



class RatingCustomerModelTestCase(TestCase): #check rating retrival
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(title="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            price=100.00,
            category=self.category,
            description="This is a test product.",
            stock=10,
            type="Sale",
            rate=4.5,
            rate_count=5,
            image="uploads/product/test_image.jpg"
        )
        self.rating = rating_custmor.objects.create(user=self.user, product=self.product)

    def test_unique_together(self):
        with self.assertRaises(Exception):
            rating_custmor.objects.create(user=self.user, product=self.product)  # Duplicate entry should raise an error



class OrderCustomerModelTestCase(TestCase): #check order per custmor retrival
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.order = order_custmor.objects.create(
            user=self.user,
            phone=1234567890,
            address="123 Test St",
            order_items="Item1, Item2"
        )

    def test_str_representation(self):
        self.assertEqual(str(self.order), "testuser")

    def test_order_fields(self):
        self.assertEqual(self.order.phone, 1234567890)
        self.assertEqual(self.order.address, "123 Test St")
        self.assertEqual(self.order.order_items, "Item1, Item2")