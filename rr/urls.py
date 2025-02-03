from django.urls import path
from . import views

# URLs
urlpatterns = [
    path('', views.place_order, name='place_order'),
    path('kitchen_orders/', views.kitchen_orders, name='kitchen_orders'),
    path('a/orders/', views.orders_view, name='admin_orders'),
    path('a/menu/', views.admin_dashboard, name='admin_menu'),
    path('todays-orders/', views.todays_orders, name='todays_orders'),
    path('a/dashboard/',views.dashboard,name='dash'),
    path('mark-not-available/<int:item_id>/', views.mark_not_available, name='mark_not_available'),
    path('mark-state/<int:item_id>/', views.mark_state, name='mark_state'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('accounts/login/',views.Login,name='login'),
    path('a/totalusers/',views.users,name='users'),





    
]
