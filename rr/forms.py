from django import forms
from .models import *

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'item', 'quantity', 'status']
