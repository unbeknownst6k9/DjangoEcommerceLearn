import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        #this is to prevent first loading with no 'cart' cookie error
        cart = {}

    print('cart python: ',cart)
    #if the user is not autenticated return an empty list of item
    items = []
    order = {'get_cart_items':0, 'get_cart_total':0, 'shipping':False}
    cartItems = order['get_cart_items']

        
    for i in cart:
        try: #if we remove the product from database, the cookie may not
            #updates with the database, and will cause an error
            #to prevent this, just pass when the product cannot load
            cartItems += cart[i]["quantity"]
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]
            item={
                'product':{
                    'id':i,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]["quantity"],
                'get_total':total,
                }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    return {'items':items, 'order':order, 'cartItems':cartItems}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        #This creates a new order by default so it will always shows a new empty order
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        #if the user is not autenticated return an empty list of item
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'items':items, 'order':order, 'cartItems': cartItems}

def guestOrder(request, data):
    print('user is not logged in')
    print('COOKIES: ', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']
    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )
    return customer, order