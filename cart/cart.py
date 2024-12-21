from core.models import Product, cart_Custmor

class Cart():
    def __init__(self, request):
        self.session = request.session 

        self.request = request

        cart = self.session.get('session_key')  # get the current session key if exists
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}  #create session key if no one exists
        self.cart = cart #to ensure the cart works in every page

    def db_add(self, product, quantity):
        product_id = str(product)
        produt_qty = str(quantity)
        if product_id in self.cart: #check if product is already in  cart
            pass
        else:
            self.cart[product_id]= int(produt_qty)
        self.session.modified = True
        current_user = cart_Custmor.objects.filter(user__id=self.request.user.id) #get the current user
        carty = str(self.cart) #change the cart to string
        carty = carty.replace("\'","\"") # replace ' with " for later 
        current_user.update(old_cart=str(carty))

    def add(self, product, quantity):
        product_id = str(product.id)
        produt_qty = str(quantity)
        if product_id in self.cart: #check if product is already in  cart
            pass
        else:
            self.cart[product_id]= int(produt_qty)
        self.session.modified = True

        current_user = cart_Custmor.objects.filter(user__id=self.request.user.id) #get the current user
        carty = str(self.cart) #change the cart to string
        carty = carty.replace("\'","\"") # replace ' with " for later 
        current_user.update(old_cart=str(carty))




    def __len__(self):
        return len(self.cart)


    def get_prods(self):
        product_ids =  self.cart.keys() #get ids from cart
        products = Product.objects.filter(id__in=product_ids) #use ids to lookup products in the database
        return products #return looked up products
    
    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        ourcart = self.cart #get cart
        ourcart[product_id] = product_qty
        self.session.modified = True

        current_user = cart_Custmor.objects.filter(user__id=self.request.user.id) #get the current user
        carty = str(self.cart) #change the cart to string
        carty = carty.replace("\'","\"") # replace ' with " for later 
        current_user.update(old_cart=str(carty))


        updatedcart = self.cart
        return updatedcart

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        current_user = cart_Custmor.objects.filter(user__id=self.request.user.id) #get the current user
        carty = str(self.cart) #change the cart to string
        carty = carty.replace("\'","\"") # replace ' with " for later 
        current_user.update(old_cart=str(carty))

  
    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    total = total + (product.price * value)

        return total