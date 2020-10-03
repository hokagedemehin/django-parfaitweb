from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import *
from .forms import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .filters import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

# @login_required(login_url='login')
def store(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    # else:
    #     items = []
    #     order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    #     cartItems = order['get_cart_items']
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'drinks/store.html', context)


def storeParfait(request, slugProduct):
    if request.user.is_authenticated:
        # products = Product.objects.get(slugProduct=slugProduct)
        # allproducts = Product.objects.exclude(name=products.name)
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        # products = Product.objects.get(slugProduct=slugProduct)
        # allproducts = Product.objects.exclude(name=products.name)
    products = Product.objects.get(slugProduct=slugProduct)
    allproducts = Product.objects.exclude(name=products.name)
    context = {'products':products, 'allproducts':allproducts, 'cartItems':cartItems}
    
    return render(request, 'drinks/store_parfait.html', context)


def cart(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    # else:
    #     cookieData = cookieCart(request)
    #     cartItems = cookieData['cartItems']
    #     order = cookieData['order']
    #     items = cookieData['items']
    # else:
        # try:
        #     cart = json.loads(request.COOKIES['cart'])
        # except:
        #     cart = {}
        # print('cart view: ' ,cart)
        # items = []
        # order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        # cartItems = order['get_cart_items']

        # for i in cart:
        #     try:

        #         cartItems += cart[i]['quantity']

        #         product = Product.objects.get(id=i)
        #         total  = (product.price * cart[i]['quantity'])

        #         order['get_cart_total'] += total
        #         order['get_cart_items'] += cart[i]['quantity']

        #         item = {
        #             'product': {
        #                 'id': product.id,
        #                 'name': product.name,
        #                 'price': product.price,
        #                 'imageURL': product.imageURL,
        #                 'records': product.records
        #             },
        #             'quantity': cart[i]['quantity'],
        #             'get_total': total,
        #         }

        #         items.append(item)
        #     except:
        #         pass
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'drinks/cart.html', context)


def checkout(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    # else:
        # items = []
        # order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        # cartItems = order['get_cart_items']
        # cookieData = cookieCart(request)
        # cartItems = cookieData['cartItems']
        # order = cookieData['order']
        # items = cookieData['items']
    testkeys = Flutter.objects.first()
    livekeys = Flutter.objects.last()
    publictest = testkeys.publicKey
    livetest = livekeys.publicKey
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'publictest': publictest, 'livetest': livetest}
    return render(request, 'drinks/checkout.html', context)


def storeDetails(request):
    context = {}
    return render(request, 'drinks/store_details.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    record = data['record']
    print('view values',action, productId, record)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    print(product, product.records)
    rec = product.stock
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    # recorded, created = Product.objects.get_or_create(records=)
    if action == 'add' and orderItem.quantity < rec:
        orderItem.quantity = (orderItem.quantity + 1)
        product.records = (int(product.records) - 1)
        print(product.records, rec)
        product.save()
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        product.records = (int(product.records) + 1)
        print(product.records, rec)
        product.save()
    elif orderItem.quantity == rec and action == 'add':
        orderItem.quantity = rec
    orderItem.save()
    
    if orderItem.quantity <= 0 or action == 'clear':
        product.records = rec
        product.save()
        orderItem.delete()

    
        

    return JsonResponse('item was added from view', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        for item in items:
            # item.product.stock = (item.product.stock - item.quantity)
            item.product.stock = item.product.records
            item.product.save()
        print(items)
        # for item in items:
        #     # item.product.stock = (item.product.stock - item.quantity)
        #     item.product.stock = item.product.records
        #     item.product.save()
        # total = float(data['form']['total'])
        # order.transaction_id = transaction_id

        # if total == order.get_cart_total:
        #     order.complete = True
        # order.save()

        # if order.shipping == True:
        #     ShippingAddress.objects.create(
        #         customer = customer,
        #         order = order,
        #         address = data['shipping']['address'],
        #         city = data['shipping']['city'],
        #         state = data['shipping']['state'],
        #         zipcode = data['shipping']['zipcode'],
        #     )
        
        if order.complete == True:
            print()
    else:
        print('user not logged in')
        customer, order = guessOrder(request, data)

    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )
        
    return JsonResponse('Payment complete for process', safe=False)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'staff'])
def parfaitDetails(request):
    products = Product.objects.all()
    productsCount = products.count()
    totalStock = 0
    for product in products:
        totalStock += product.stock
    cartItems = cartData(request)['cartItems']
    ordersCount = Order.objects.all().count()
    customersCount = Customer.objects.all().count()
    delivered = Order.objects.filter(complete='True').count()
    customers = Customer.objects.all()
    context={'products': products,'totalStock': totalStock,'productsCount': productsCount, 'customers': customers,'ordersCount': ordersCount,'customersCount': customersCount,'delivered': delivered, 'cartItems': cartItems}
    return render(request, 'drinks/parfaits.html', context)


def ParfaitUpdate(request, slugProduct):
    product = Product.objects.get(slugProduct = slugProduct)
    cartItems = cartData(request)['cartItems']
    name = product.name
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES,  instance=product)
        if form.is_valid():
            form.save()
            return redirect('parfait')
    context = {'form': form, 'name': name, 'cartItems': cartItems}
    return render(request, 'drinks/parfait_update.html', context)


def ParfaitDelete(request, slugProduct):
    product = Product.objects.get(slugProduct = slugProduct)
    cartItems = cartData(request)['cartItems']
    if request.method == 'POST':
        product.delete()
        return redirect('parfait')

    context = {'product':product, 'cartItems': cartItems}
    return render(request, 'drinks/parfait_delete.html', context)


def parfaitCreate(request):
    form = ProductForm()
    cartItems = cartData(request)['cartItems']
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('parfait')
    context = {'form': form, 'cartItems': cartItems}
    return render(request, 'drinks/parfait_create.html', context)

def allOrders(request):
    orders = Order.objects.all().order_by('-date_ordered')
    ordersCount = Order.objects.all().count()
    delivered = Order.objects.filter(status='Delivered').count()
    pendingCount = Order.objects.filter(status='Pending').count()
    OutDeliveryCount = Order.objects.filter(status='Out for Delivery').count()
    cartItems = cartData(request)['cartItems']
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    page = request.GET.get('page')
    paginator = Paginator(orders, 10)

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    context = {'orders': orders, 'pendingCount':pendingCount,'OutDeliveryCount': OutDeliveryCount,'cartItems': cartItems, 'myFilter':myFilter,'ordersCount': ordersCount, 'delivered': delivered}
    return render(request, 'drinks/orders.html', context)


def OrdersDetails(request, slugOrder):
    orderDetail = Order.objects.get(slugOrder = slugOrder)
    cartItems = cartData(request)['cartItems']
    name = orderDetail.customer.name
    form = OrderForm(instance=orderDetail)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=orderDetail)
        if form.is_valid():
            form.save()
            return redirect('orders')
    context = {'form': form, 'orderDetail':orderDetail, 'name': name, 'cartItems': cartItems}
    return render(request, 'drinks/orders_detail.html', context)


def orderItemsDetails(request):
    orderItems = OrderItem.objects.all().order_by('-order')
    orderItemCount = orderItems.count()
    ordersCount = Order.objects.all().count()
    pendingCount = Order.objects.filter(status='Pending').count()
    customers = Customer.objects.all()
    cartItems = cartData(request)['cartItems']
    myFilter = OrderItemFilter(request.GET,queryset=orderItems)
    # myCustomerFilter = CustomerFilter(request.GET, queryset=customers)
    orderItems = myFilter.qs
    # customers = myCustomerFilter.qs
    page = request.GET.get('page')
    paginator = Paginator(orderItems, 10)

    try:
        orderItems = paginator.page(page)
    except PageNotAnInteger:
        orderItems = paginator.page(1)
    except EmptyPage:
        orderItems = paginator.page(paginator.num_pages)
    context = {'orderItems': orderItems,'orderItemCount':orderItemCount ,'ordersCount':ordersCount ,'pendingCount':pendingCount,'customers': customers, 'cartItems': cartItems, 'myFilter':myFilter}
    return render(request, 'drinks/orderItems.html', context)

def customer(request):
    customers = Customer.objects.all()
    orders = Order.objects.all().filter(complete=True)
    totalPayment = 0
    for order in orders:
        totalPayment += order.get_cart_total
    customersCount = Customer.objects.all().count()
    paymentsCount = Order.objects.filter(complete=True).count()
    cartItems = cartData(request)['cartItems']

    page = request.GET.get('page')
    paginator = Paginator(customers, 5)

    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)


    context={'customers': customers,'totalPayment': totalPayment,'paymentsCount': paymentsCount,'customersCount': customersCount,'cartItems': cartItems}
    return render(request, 'drinks/customer.html', context)


def customerDetails(request, slugCustomer):
    customers = Customer.objects.get(slugCustomer=slugCustomer)
    ordersCount = Order.objects.all().filter(customer__name = customers.name).count()
    orders = customers.order_set.all()
    orders1 = Order.objects.all().filter(customer__name = customers.name, complete=True)
    totalPayment = 0
    for order in orders1:
        totalPayment += order.get_cart_total
    orderItems = OrderItem.objects.filter(order__customer__name = customers.name).order_by('-date_added')
    myFilter = CustomerFilter(request.GET,queryset=orderItems)
    orderItems = myFilter.qs
    # ordersCount = orders.count()
    cartItems = cartData(request)['cartItems']
    
    # orders = Order.objects.filter(customer = customers.name)
    # orderItems = OrderItem.objects.all().filter()
    
    page = request.GET.get('page')
    paginator = Paginator(orderItems, 3)

    try:
        orderItems = paginator.page(page)
    except PageNotAnInteger:
        orderItems = paginator.page(1)
    except EmptyPage:
        orderItems = paginator.page(paginator.num_pages)

    context = {'customers':customers, 'totalPayment': totalPayment,'orders':orders,'orderItems':orderItems,'ordersCount':ordersCount,'cartItems': cartItems, 'myFilter':myFilter}
    
    return render(request, 'drinks/customer_details.html', context)


def sendEmail(request):
    if request.method == 'POST':
        template = render_to_string('drinks/email_template.html', {
            'name': request.POST['lastName'],
            'email': request.POST['email'],
            'message': request.POST['message'],
        })
        email = EmailMessage(
            request.POST['title'],
            template,
            settings.EMAIL_HOST_USER,
            ['demehin.george@gmail.com']
        )
        email.fail_silently = False
        email.send()
    return render(request, 'drinks/email_sent.html')

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            # Customer.objects.create(user=user, name=user.first_name, email=user.email)
            first_name = form.cleaned_data.get('first_name')
            messages.success(request, 'New Account was created for ' + first_name)
            return redirect('login')
    context={'form': form, }
    return render(request, 'drinks/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
            # return redirect(request.GET['next'])
        else:
            messages.info(request, 'Username or Password is incorrect')
            # return render(request, 'drinks/login.html')
    context={}
    return render(request, 'drinks/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('store')

def userPage(request):
    cartItems = cartData(request)['cartItems']
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(complete=True).count()
    customers = Customer.objects.get(user = request.user)
    orderItems = OrderItem.objects.filter(order__customer__name = customers.name).order_by('-order')
    myFilter = CustomerFilter(request.GET,queryset=orderItems)
    orderItems = myFilter.qs

    page = request.GET.get('page')
    paginator = Paginator(orderItems, 5)

    try:
        orderItems = paginator.page(page)
    except PageNotAnInteger:
        orderItems = paginator.page(1)
    except EmptyPage:
        orderItems = paginator.page(paginator.num_pages)

    context={'orders':orders,'total_orders':total_orders, 
    'delivered':delivered, 'cartItems': cartItems, 'orderItems': orderItems, 
    'customers': customers, 'myFilter': myFilter}
    return render(request, 'drinks/user.html', context)

def notUserPage(request):
    cartItems = cartData(request)['cartItems']
    context={'cartItems': cartItems}
    return render(request, 'drinks/user_not.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def StaffPage(request):
    form = CreateStaffForm()
    cartItems = cartData(request)['cartItems']
    if request.method == 'POST':
        form = CreateStaffForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='staff')
            user.groups.add(group)
            first_name = form.cleaned_data.get('first_name')
            messages.success(request, 'New Staff Account was created for ' + first_name)
            return redirect('store')
    context={'form': form, 'cartItems': cartItems }
    return render(request, 'drinks/staff.html', context)

def ProfilePage(request):
    customer = request.user.customer
    cartItems = cartData(request)['cartItems']
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully')

    context = {'form':form, 'cartItems': cartItems}
    return render(request, 'drinks/profile.html', context)
