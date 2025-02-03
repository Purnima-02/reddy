from django.contrib import admin

from .models import Order, UserProfile, KitchenOrder, Menu, MenuItem
# Admin Panel
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'cabin', 'phone', 'status', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('name', 'cabin', 'phone')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cabin', 'phone')
    search_fields = ('user__username', 'cabin', 'phone')

@admin.register(KitchenOrder)
class KitchenOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'is_prepared', 'prepared_at')
    list_filter = ('is_prepared',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('date',)
    filter_horizontal = ('items',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'available')
    list_filter = ('available',)
    search_fields = ('name',)
