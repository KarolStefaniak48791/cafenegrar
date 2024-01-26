from django.shortcuts import render, redirect
from .models import Coffee
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Coffee, Order, OrderItem, Reservation
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import HttpResponse

def index(request):
    if request.method == "POST":
        message = request.POST['message']
        email = request.POST['email']
        name = request.POST['name']
        subject = request.POST['subject']
        send_mail(
            subject,
            f"Message from {name}, {message}",
            "settings.EMAIL_HOST_USER",
            [email, "first@example.com", "other@example.com"],
            fail_silently=False) 
    return render(request, "homepage.html")

def loginPage(request):
    if request.method ==  'POST':
        if 'login_button' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = User.objects.get(username=username)
            except:
                messages.error(request, "User does not exist")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Username or password does not exist")
        if 'register_button' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                User.objects.create_user(username=username, password=password, email=email)
                user = authenticate(request, username=username, password=password)
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Account Already Exist")
    context = {}
    return render(request, "login.html", context)


def onas(request):
    return render(request, "about.html")

def menu(request):
    amount = [x for x in range (10)]
    coffees = Coffee.objects.all()
    return render(request, "menu.html", {'coffees': coffees,'amount': amount })

@login_required(login_url="login")
def profil(request):
    user_orders = Order.objects.filter(customer_id=request.user.id)
    orders_with_items = []
    for order in user_orders:
        items = OrderItem.objects.filter(order=order)
        orders_with_items.append((order, items))
    user_reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'profil.html', {'orders_with_items': orders_with_items, 'user_reservations': user_reservations})

@login_required(login_url='login')
def order_view(request):
    if request.method == 'POST':
        selected_coffees = request.POST.getlist('coffees')
        order = Order.objects.create(
            customer_id=request.user.id,
            cost=0
        )
        total_cost = 0
        for selected_coffee in selected_coffees:
            coffee_id, quantity = map(int, selected_coffee.split(':'))
            coffee = Coffee.objects.get(pk=coffee_id)
            if quantity > 0:
                OrderItem.objects.create(order=order, coffee=coffee, quantity=quantity)
                total_cost += coffee.price * quantity
        order.cost = total_cost
        order.save()
        return redirect('dziekujemy-zamowienie')
    coffees = Coffee.objects.all()
    return render(request, 'menu.html', {'coffees': coffees})

def dziekujemy_zamowienie(request):
    return render(request, "dziekujemy-zamowienie.html")
    
def logout_view(request):
    logout(request)
    return redirect('/')

def rezerwacja(request):
    return render(request, "rezerwacja.html")
    
@login_required(login_url='login')
def reserve_table(request):
    if request.method == 'POST':
        data = request.POST
        print('Received data:', data)
        selected_table_ids = data.getlist('selectedTableIds[]', [])
        number_of_hours = int(data.get('numberOfHours', 0))
        selected_date_str = data.get('selectedDate', '')
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Szczegółowy komunikat o błędzie'})

        reservation_cost = float(data.get('reservationCost', 0))
        user = request.user  # Pobierz zalogowanego użytkownika
        reservation = Reservation(
            user=user,
            table_ids=selected_table_ids,
            number_of_hours=number_of_hours,
            selected_date=selected_date,
            reservation_cost=reservation_cost
        )
        reservation.save()  
        return HttpResponse('Dziękujemy za rezerwację!')
    else:
        return redirect('dziekujemy-rezerwacja')
    
def dziekujemy_rezerwacja(request):
    return render(request, "dziekujemy-rezerwacja.html")
