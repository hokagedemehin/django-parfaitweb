import django_filters
from .models import *
from django_filters import DateFilter, CharFilter

class OrderItemFilter(django_filters.FilterSet):
    Date_ordered = DateFilter(field_name="date_added", lookup_expr='lte')
    Date_ordered_2 = DateFilter(field_name="date_added", lookup_expr='gte')
    # order__customer = CharFilter()
    # start_date = DateFilter(field_name="date_created", lookup_expr='gte')
    # end_date = DateFilter(field_name="date_created", lookup_expr='lte')
    # note = CharFilter(field_name='note', lookup_expr='icontains')
    class Meta:
        model = OrderItem
        fields = ['product', 'order', 'order__customer']
        exclude = ['quantity', 'ship', 'slugOrderitem']

class CustomerFilter(django_filters.FilterSet):
    Date_ordered = DateFilter(field_name="date_added", lookup_expr='lte')
    Date_ordered_2 = DateFilter(field_name="date_added", lookup_expr='gte')
    class Meta:
        model = OrderItem
        fields = ['product', 'order']

# class OrderItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
#     ship = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
#     quantity = models.IntegerField(default=0, null=True, blank=True)
#     date_added = models.DateTimeField(auto_now_add=True)
#     slugOrderitem = models.SlugField(null=True, blank=True)