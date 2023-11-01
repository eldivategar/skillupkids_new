from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .helpers.decorators import user_must_be_registered
from user_pages.models import Member, Mitra
from .helpers.utils import send_otp, get_customer_data
from datetime import datetime
import pyotp

def home(request):
    if 'customer_id' not in request.session:
        return render(request, 'landing_page/index.html')

    data = get_customer_data(request)
    return render(request, 'landing_page/index.html', {'data': data})

def about(request):
    if 'customer_id' not in request.session:
        return render(request, 'landing_page/about.html')
    
    data = get_customer_data(request)
    return render(request, 'landing_page/about.html', {'data': data})

def contact(request):
    if 'customer_id' not in request.session:
        return render(request, 'landing_page/contact.html')
    
    data = get_customer_data(request)
    return render(request, 'landing_page/contact.html', {'data': data})

def login(request):
    if request.method == 'GET':
        return render(request, 'landing_page/login.html')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            member = Member.objects.filter(email=email).first()
            mitra = Mitra.objects.filter(email=email).first()

            if member:
                if check_password(password, member.password):
                    request.session['customer_id'] = member.uuid_str()
                    # request.session['user_type'] = 'member'
                    return redirect('user_pages:member_profile')
                else:
                    messages.error(request, 'Ups, Password salah!')
                    return redirect('login')

            if mitra:
                if check_password(password, mitra.password):
                    request.session['customer_id'] = mitra.uuid_str()
                    # request.session['user_type'] = 'mitra'
                    return redirect('home')
                else:
                    messages.error(request, 'Ups, Password salah!')
                    return redirect('login')
                                
            else: 
                messages.error(request, 'Email belum terdaftar di SkillUpKids!')
                return redirect('login')

def register(request):
    if request.method == 'GET':        
        return render(request, 'landing_page/register.html')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('num_wa')
        password = request.POST.get('password')
        
        if name and email and number and password:            
            if Member.objects.filter(email=email).exists():
                messages.error(request, 'Email sudah terdaftar!')
                return redirect('register')
                        
            if Member.objects.filter(number=number).exists():
                messages.error(request, 'Nomor whatsapp sudah terdaftar!')
                return redirect('register')
            
            request.session.flush()
            import uuid
            unique_code = str(uuid.uuid4())
            request.session['unique_code'] = unique_code 
            
            request.session['name'] = name
            request.session['email'] = email
            request.session['number'] = number
            request.session['password'] = password
            request.session.set_expiry(300)

            send_otp(request, email)          
            messages.success(request, 'Kode berhasil dikirim ke email anda!')

            return redirect('verify')
        else:
            return redirect('register')
    
@user_must_be_registered
def verify(request):
    
    if request.method == 'GET':
        return render(request, 'landing_page/verify.html')

    if request.method == 'POST':
        user_otp = request.POST.get('digit-1') + request.POST.get('digit-2') + request.POST.get('digit-3') + request.POST.get('digit-4')
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_until = request.session['otp_valid_until']

        if otp_secret_key and otp_valid_until is not None:
            valid_until = datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, digits=4, interval=60)

                if totp.verify(user_otp):
                    name = request.session['name']
                    email = request.session['email']
                    number = request.session['number']
                    password = request.session['password']

                    customer = Member(name=name, email=email, number=number, password=password, is_verified=True)
                    customer.save()

                    request.session.clear()
                    request.session['customer_id'] = customer.uuid_str()
                    messages.success(request, 'Akun berhasil dibuat!')
                    return redirect('home')
                
                else:
                    messages.error(request, 'Kode OTP salah!')
                    return redirect('verify')
            
            else:
                messages.error(request, 'Kode OTP sudah kadaluarsa!')
                return redirect('verify')

        else:
            messages.error(request, 'Ups...terjadi kesalahan, silahkan coba lagi!')
            return redirect('verify')

def logout(request):
    request.session.flush()
    return redirect('home')

def _404(request, exception):
    return render(request, 'errors/error-404.html')

def _500(request):
    return render(request, 'errors/error-500.html')
