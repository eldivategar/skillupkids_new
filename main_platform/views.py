from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import Customer

def home(request):
    return render(request, 'landing_page/index.html')

def about(request):
    return render(request, 'landing_page/about.html')

def contact(request):
    return render(request, 'landing_page/contact.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'landing_page/login.html')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            customer = Customer.objects.get(email=email)
            if customer:
                if check_password(password, customer.password):
                    return redirect('home')
                messages.error(request, 'Ups, Password salah!')
                return redirect('login')
            
            messages.error(request, 'Email belum terdaftar di SkillUpKids!')
            return redirect('login')

def register(request):
    if request.method == 'GET':        
        return render(request, 'landing_page/register.html')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('num_wa')
        password = request.POST.get('confirm-password')
        
        if name and email and number and password:            
            if Customer.objects.filter(email=email).exists():
                messages.error(request, 'Email sudah terdaftar!')
                return redirect('register')
                        
            if Customer.objects.filter(number=number).exists():
                messages.error(request, 'Nomor whatsapp sudah terdaftar!')
                return redirect('register')
            
            customer = Customer(name=name, email=email, number=number, password=password)
            customer.save()            
            messages.success(request, 'Your account has been created!')

            return redirect('login')
        else:
            return redirect('register')
    

def verify_otp(request):
    return render(request, 'landing_page/verify_otp.html')

def page_not_found(request, exception):
    return render(request, 'errors/404.html')