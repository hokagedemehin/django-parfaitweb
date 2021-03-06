from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import *

@receiver(post_save, sender=User)
def customer_profile(sender, instance, created, **kwargs):
    if created:
        # group = Group.objects.get(name='customer')
        # instance.groups.add(group)
        Customer.objects.create(user=instance, name=instance.first_name, email=instance.email)

@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if created == False:
        instance.customer.save()