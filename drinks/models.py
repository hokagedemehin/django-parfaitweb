from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# from ckeditor.fields import RichTextField
# Create your models here.
# null is for back end, blank is for front end

# for a time that you can change do the following
# from django.utils import timezone
# date_added = models.DateTimeField(default=timezone.now)
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=1000, null=True)
    profile_pic = models.ImageField(default = "profile_default.jpg",null=True, blank=True)
    slugCustomer = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name or ''

    def save(self, *args, **kwargs):
        if self.slugCustomer == None:
            slugCustomer = slugify(self.name)

            has_slug = Customer.objects.filter(slugCustomer = slugCustomer).exists()
            count = 1
            while has_slug:
                count += 1
                slugCustomer = slugify(self.name) + '-' + str(count)
                has_slug = Customer.objects.filter(slugCustomer=slugCustomer).exists()
            self.slugCustomer = slugCustomer

        super().save(*args, **kwargs)

    

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    full_description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    records = models.IntegerField(default=0, null=True, blank=True)
    stock = models.IntegerField(default=0, null=True, blank=True)
    slugProduct = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name or ''

    @property
    def imageURL(self):
        try: 
            url = self.image.url
        except:
            url=''
        return url
    
    def save(self, *args, **kwargs):
        if self.slugProduct == None:
            slugProduct = slugify(self.name)

            has_slug = Product.objects.filter(slugProduct=slugProduct).exists()
            count = 1
            while has_slug:
                count += 1
                slugProduct = slugify(self.name) + '-' + str(count)
                has_slug = Product.objects.filter(slugProduct=slugProduct).exists()
            self.slugProduct = slugProduct

        super().save(*args, **kwargs)


class Order(models.Model):
    # STATUS = (
    #     ('Pending', 'Pending'),
    #     ('Delivered','Delivered'),
    # )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True) 
    date_ordered = models.DateTimeField(auto_now_add=True)
    # ship = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, null=True, blank=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True)
    slugOrder = models.SlugField(null=True, blank=True)
    # status = models.CharField(max_length=100, null=True, blank=True, choices=STATUS)
    

    def __str__(self):
        return str(self.id) or ''
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    def save(self, *args, **kwargs):
        if self.slugOrder == None:
            slugOrder = slugify(self.customer.name)

            has_slug = Order.objects.filter(slugOrder = slugOrder).exists()
            count = 1
            while has_slug:
                count += 1
                slugOrder = slugify(self.customer.name) + '-' + str(count)
                has_slug = Order.objects.filter(slugOrder=slugOrder).exists()
            self.slugOrder = slugOrder

        super().save(*args, **kwargs)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, default=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    ship = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    slugOrderitem = models.SlugField(null=True, blank=True)

    # class Meta:
    #     ordering = ['order']

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    





