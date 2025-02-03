from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Menu, OrderItem, MenuItem,Order
from datetime import datetime
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def place_order(request):
    # Fetch only available items where `not_available=False` and `state=True`
    menu_items = MenuItem.objects.filter(available=True, not_available=False, state=True)

    if request.method == "POST":
        order = Order.objects.create(
            name=request.POST['name'],
            cabin=request.POST['cabin'],
           
        )

        selected_items = request.POST.getlist('order_items')  # List of selected item IDs

        for item_id in selected_items:
            item = MenuItem.objects.get(id=item_id)
            quantity = int(request.POST.get(f'quantity_{item_id}', 1))  # Get quantity for the item
            OrderItem.objects.create(order=order, item=item, quantity=quantity)

        return HttpResponse('ok')  # Redirect after placing the order

    return render(request, 'orders/user_order.html', {'menu_items': menu_items})

@csrf_exempt
def kitchen_orders(request):
    # Fetch only orders that are still in progress
    orders = Order.objects.filter(status__in=['pending', 'preparing'])

    if request.method == "POST":
        order = get_object_or_404(Order, id=request.POST['order_id'])
        order.status = request.POST['status']
        order.save()

    return render(request, 'orders/kitchen_orders.html', {'orders': orders})

@csrf_exempt
def admin_dashboard(request):
    """View to manage the menu: add items & manage availability"""
    
    menu = Menu.objects.first()
    if not menu:
        menu = Menu.objects.create()

    if request.method == "POST":
        new_item_name = request.POST.get('name')
        item_id = request.POST.get('toggle_availability')

        if new_item_name:
            # Add new menu item with default availability
            menu_item = MenuItem.objects.create(
                name=new_item_name,
                available=True,    # Ensure item is available by default
                not_available=False,
                state=True
            )
            menu.items.add(menu_item)
            menu.save()
            print(f"Item '{new_item_name}' added to the menu.")
            return redirect('admin_menu')

        if item_id:
            # Toggle availability of an item
            item = MenuItem.objects.get(id=item_id)
            item.not_available = not item.not_available  # Toggle availability
            item.state = not item.not_available  # Ensure state is False if not_available is True
            item.available = not item.not_available  # Adjust available flag
            item.save()
            messages.success(request, "Item added successfully!")
            print(f"Item '{item.name}' availability changed.")
            return redirect('admin_menu')

    menu_items = menu.items.all()
    return render(request, 'orders/admin_dashboard.html', {'menu': menu, 'menu_items': menu_items})


def orders_view(request):
    orders = Order.objects.prefetch_related('orderitems__item').all()  # Optimized query
    print("Orders Data:", orders)  # Debugging output

    for order in orders:
        print(f"Order: {order.name}, Status: {order.status}")
        for order_item in order.orderitems.all():
            print(f"  - Item: {order_item.item.name}, Quantity: {order_item.quantity}")

    return render(request, 'orders/view_orders.html', {'orders': orders})


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import MenuItem

def mark_not_available(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(MenuItem, id=item_id)
        item.not_available = True
        item.state = False  # Ensure state is False
        item.available = False  # Ensure availability reflects the change
        item.save()

        return JsonResponse({"status": "success", "message": f"'{item.name}' marked as Not Available."})

    return JsonResponse({"status": "error", "message": "Invalid request method."})


# Mark the item as Available
def mark_state(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(MenuItem, id=item_id)
        item.state = True
        item.not_available = False  # Ensure not_available is False
        item.available = True  # Item is available again
        item.save()

        return JsonResponse({"status": "success", "message": f"'{item.name}' marked as Available (State)."})
    
    return JsonResponse({"status": "error", "message": "Invalid request method."})




def todays_orders(request):
    today = datetime.now().date()
    orders = Order.objects.filter(timestamp__date=today).prefetch_related('orderitems__item')
    print("Orders Data:")
    for order in orders:
        print(f"Order: {order.name}, Status: {order.status}")
        for order_item in order.orderitems.all():
            print(f"  - Item: {order_item.item.name}, Quantity: {order_item.quantity}")

    return render(request, 'orders/today_orders.html', {'orders': orders})
from django.utils import timezone

def dashboard(request):
    today = timezone.now().date()  # Get today's date

    menu = Menu.objects.first()
    menu_count = menu.items.count() if menu else 0

    total_orders = Order.objects.count()

    # Count today's orders
    todays_orders = Order.objects.filter(timestamp__date=today).count()
    total_users = User.objects.count()
    # Count menu items added today
    todays_menu_count = MenuItem.objects.filter(created_at__date=today).count()

    context = {
        'menu_count': menu_count,
        'total_orders': total_orders,
        'todays_orders': todays_orders,
        'todays_menu_count': todays_menu_count,
        'total_users':total_users 
    }
    
    return render(request, 'orders/dashboard.html', context)

from django.contrib.auth.models import User
from django.contrib import auth
@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return HttpResponse("user already exists")
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already taken.')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                request.session['registration_successful'] = True
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
    else:
        return render(request, 'orders/register.html')

@csrf_exempt
def Login(request):
    if request.method == 'POST':#IF THE CONDITION IS TRUE IT SHOULD ENTER INTO THE IF CONDITION
       username = request.POST['username'] 
       password = request.POST['password']  

       user = auth.authenticate(username=username,password=password)
       if user is not None:
           auth.login(request, user)
           print('login is successfully')
           return redirect('dash')
       else:
           print('invalid credentials')
           return redirect('login')
    else:
        return render(request,'orders/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        print("logged out successfully")
        return redirect('login')    
        
def users(request):
    data=User.objects.all()
    return render(request,'orders/total_users.html',{'data':data})
