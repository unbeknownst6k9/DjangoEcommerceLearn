from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# This creates one to one model between user and customer
# 1 customer can only have 1 user
# null = True means the data in the DB can be null
# blank = True means the website form can be set to empty which may cause error if the code require the attribute
class Customer(models.Model):
    #allow user name to be null and on this model is deleted it also delete the user
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    #The default determines if the product is digital and needed to be shipped
    #false means it is not digital and needed to be shipped
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(default='placeholder.png')
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
             url = ''
        return url


#set up relationship with the customer where a cusomter can have many orders
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    Transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()
        #loop through all product
        #if product
        for item in order_items:
            if not (item.product.digital):
                shipping= not item.product.digital
                return shipping
        return shipping

    #This method is for counting the price for all items in cart
    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    #This method is for counting all the items in cart
    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

#A single order can have many order items
class OrderItem(models.Model):
     product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
     order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
     quantity = models.IntegerField(default=0, null=True, blank=True)
     date_added = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return self.product.name
     @property
     def get_total(self):
          return self.product.price * self.quantity
     
class ShippingAddress(models.Model):
     #if the order gets deleted mid-way the customer field can still validate the order
     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
     order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
     address = models.CharField(max_length=200, null=True)
     city = models.CharField(max_length=200, null=True)
     province = models.CharField(max_length=200, null=True)
     postal_code = models.CharField(max_length=200, null=True)

     def __str__(self):
          return self.address