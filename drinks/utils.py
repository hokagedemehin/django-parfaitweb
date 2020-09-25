import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('cart view util: ' ,cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:

            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total  = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                    'records': cart[i]['records'],
                    'stock': product.stock,
                    'slugProduct': product.slugProduct
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }

            items.append(item)
            if product.digital == False:
                order['shipping'] = True
            
        except:
            pass
    
    return {'cartItems': cartItems, 'order':order, 'items':items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems': cartItems, 'order':order, 'items':items}

def guessOrder(request, data):
    print('User is not logged in...')
    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']
    print(items)
    customer, created = Customer.objects.get_or_create(email=email, )
    customer.name = name
    customer.save()

    order = Order.objects.create( customer=customer, complete=False, )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create( product=product, order=order, quantity=item['quantity'] )
        product.stock = product.stock - orderItem.quantity
        product.records = product.stock
        product.save()
        print(product.stock)
    return customer, order



    # for item in items:
    #         # item.product.stock = (item.product.stock - item.quantity)
    #         item.product.stock = item.product.records
    #         item.product.save()
    #     print(items)