from django.shortcuts import render
from .models import MenuCategory
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count



def index(request):
    return render(request, 'index.html')

def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    return render(request, 'logout.html')

@login_required
def admin_view(request):
    return render(request, 'admin.html')

@login_required
def manager_view(request):
    return render(request, 'manager.html')

@login_required
def menu_view(request):
    return render(request, 'menu.html')

@login_required
def orders_view(request):
    return render(request, 'orders.html')

@login_required
def qr_view(request):
    return render(request, 'qr-code.html')

@login_required
def staff_view(request):
    return render(request, 'staff.html')

@login_required
def menu_view(request):
    categories = MenuCategory.objects.prefetch_related('items').all()
    table_number = request.GET.get('table', '')
    return render(request, 'menu.html', {
        'categories': categories,
        'table_number': table_number
    })



@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Role-based redirection
            if role == 'manager':
                return redirect('manager')
            elif role == 'staff':
                return redirect('staff')
            else:
                return redirect('index')  # user or general access
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('login')

    return render(request, 'signup.html')

from .models import Order, OrderItem, MenuItem

@login_required
def submit_order_view(request):
    if request.method == 'POST':
        table_number = request.POST.get('table_number')
        item_ids = request.POST.getlist('items')

        if not item_ids:
            return render(request, 'menu.html', {'categories': MenuCategory.objects.all(), 'error': 'No items selected'})

        order = Order.objects.create(
            customer=request.user,
            table_number=table_number
        )

        for item_id in item_ids:
            menu_item = MenuItem.objects.get(id=item_id)
            OrderItem.objects.create(order=order, menu_item=menu_item)

        return render(request, 'order_confirmation.html', {'order': order})

    return redirect('menu')

from .models import Order

@login_required
def staff_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.select_related('customer').prefetch_related('items__menu_item').order_by('-created_at')
    return render(request, 'staff_dashboard.html', {'orders': orders})

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

@csrf_exempt
@login_required
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
    return redirect('staff_dashboard')

    from django.db.models import Count

@login_required
def manager_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Count orders by status
    status_counts = Order.objects.values('status').annotate(count=Count('id'))
    summary = {status['status']: status['count'] for status in status_counts}

    total_orders = Order.objects.count()
    recent_orders = Order.objects.order_by('-created_at')[:10]

    return render(request, 'manager_dashboard.html', {
        'summary': summary,
        'total_orders': total_orders,
        'recent_orders': recent_orders,
    })

