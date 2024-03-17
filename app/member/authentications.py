from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from app.helpers.decorators import user_must_be_registered
from app.models import Member
from app.helpers.utils import send_otp
from datetime import datetime
import pyotp

def login(request):
    if request.method == 'GET':
        if request.session.get('customer_id'):
            next_url = request.session.get('next_url')
            return redirect(f'app.member:{next_url}' if next_url else 'app.member:member_dashboard_activity')
        return render(request, 'member/auth/login.html')
    
    if request.method == 'POST':
        # request.session.flush()
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            member = Member.objects.filter(email=email).first()

            if member:
                if check_password(password, member.password):
                    customer_uuid = f'me{member.uuid_str()}'
                    request.session['customer_id'] = customer_uuid

                    next_url = request.session.get('next_url')
                    if next_url:
                        del request.session['next_url']
                        return redirect(next_url)
                    else:
                        return redirect('app.member:member_dashboard_activity')
                else:
                    messages.error(request, 'Ups, Password salah!')
                    return redirect('app.member:login')

            else:
                messages.error(request, 'Email belum terdaftar di SkillUpKids!')
                return redirect('app.member:login')

def register(request):
    if request.method == 'GET':        
        return render(request, 'member/auth/register.html')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('num_wa')
        password = request.POST.get('password')
        
        if name and email and number and password:            
            if Member.objects.filter(email=email).exists():
                messages.error(request, 'Email sudah terdaftar!')
                return redirect('app.member:register')
                        
            if Member.objects.filter(number=number).exists():
                messages.error(request, 'Nomor whatsapp sudah terdaftar!')
                return redirect('app.member:register')
            
            request.session.flush()
            import uuid
            unique_code = str(uuid.uuid4())
            request.session['unique_code'] = unique_code 
            
            request.session['name'] = name
            request.session['email'] = email
            request.session['number'] = number
            request.session['password'] = password
            # request.session.set_expiry(300)

            send_otp(request, email)          
            messages.success(request, 'Kode berhasil dikirim ke email anda!')

            return redirect('app.member:verify')
        else:
            return redirect('app.member:register')
    
@user_must_be_registered
def verify(request):
    
    if request.method == 'GET':
        return render(request, 'member/auth/verify.html')

    if request.method == 'POST':
        user_otp = request.POST.get('digit-1') + request.POST.get('digit-2') + request.POST.get('digit-3') + request.POST.get('digit-4')
        user_otp = int(user_otp)
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

                    member = Member(name=name, email=email, number=number, password=password, is_verified=True)
                    member.save()

                    request.session.flush()
                    customer_uuid = f'me{member.uuid_str()}'
                    request.session['customer_id'] = customer_uuid
                    return redirect('app.member:member_dashboard_activity')
                
                else:
                    messages.error(request, 'Kode OTP salah!')
                    return redirect('app.member:verify')
            
            else:
                messages.error(request, 'Kode OTP sudah kadaluarsa!')
                return redirect('app.member:verify')

        else:
            messages.error(request, 'Ups...terjadi kesalahan, silahkan coba lagi!')
            return redirect('app.member:verify')
        
@user_must_be_registered
def resend_code(request):
    if request.method == 'GET':
        email = request.session.get('email')
        send_otp(request, email)
        messages.success(request, 'Kode berhasil dikirim ke email anda!')
        return redirect('app.member:verify')

def forgot_password(request):
    if request.method == 'GET':
        return render(request, 'member/auth/forgot-password.html')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if email:
            if Member.objects.filter(email=email).exists():
                if password == confirm_password:
                    member = Member.objects.get(email=email)
                    member.password = password
                    member.save()
                    messages.success(request, 'Password berhasil diubah!')
                    return redirect('app.member:login')
                else:
                    messages.error(request, 'Password tidak sama!')                
                return redirect('app.member:forgot_password')
            else:
                messages.error(request, 'Email belum terdaftar!')
                return redirect('app.member:forgot_password')
        else:
            messages.error(request, 'Ups...terjadi kesalahan, silahkan coba lagi!')
            return redirect('app.member:forgot_password')