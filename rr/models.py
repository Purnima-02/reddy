from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import path

# Menu Item Model
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    not_available=models.BooleanField(default=False)
    state=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-created_at']

    def save(self, *args, **kwargs):
        # Ensure that only one of `not_available` or `state` is `True`
        if self.not_available:
            self.state = False  # If `not_available` is True, set `state` to False
        elif self.state:
            self.not_available = False  # If `state` is True, set `not_available` to False

        super(MenuItem, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

# Menu Model for Daily Updates
class Menu(models.Model):
    date = models.DateField(auto_now_add=True)
    items = models.ManyToManyField(MenuItem)
    
    def __str__(self):
        return f"Menu for {self.date}"
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('completed', 'Completed')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Make user optional
    name = models.CharField(max_length=100)
    cabin = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    order_items = models.ManyToManyField(MenuItem)  # Link to menu items
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-timestamp'] 
    def __str__(self):
        return f"{self.name} - {', '.join([item.name for item in self.order_items.all()])} ({self.status})"


# User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cabin = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.user.username

# Chef/Kitchen Panel
class KitchenOrder(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    is_prepared = models.BooleanField(default=False)
    prepared_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Kitchen Order - {self.order.id} ({'Prepared' if self.is_prepared else 'Pending'})"
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item.name} x {self.quantity}"

