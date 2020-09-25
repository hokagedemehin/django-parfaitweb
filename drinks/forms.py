from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.label
        
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1','password2',]

class CreateStaffForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.label
        
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email','groups', 'is_staff','is_superuser', 'password1','password2',]

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']