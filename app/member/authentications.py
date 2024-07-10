from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from app.helpers.decorators import is_registering
from app.models import Member
from app.helpers.utils import send_otp, verify_otp
from datetime import datetime

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
            
            request.session['name'] = name
            request.session['email'] = email
            request.session['number'] = number
            request.session['password'] = password
            request.session['is_registering'] = True

            if send_otp(email):
                messages.success(request, 'Kode berhasil dikirim ke email anda!')                
                return redirect('app.member:verify')            
            else:
                messages.error(request, 'Gagal mengirim kode OTP, Coba beberapa saat lagi!')
                return redirect('app.member:register')
    
@is_registering
def verify(request):    
    if request.method == 'GET':
        return render(request, 'member/auth/verify.html')

    if request.method == 'POST':
        user_otp = ''.join([request.POST.get(f'digit-{i}') for i in range(1, 5)])
        email = request.session['email']

        if verify_otp(email, user_otp):
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
            messages.error(request, 'Kode OTP salah atau sudah kadaluarsa!')
            return redirect('app.member:verify')
        
@is_registering
def resend_code(request):
    if request.method == 'GET':
        email = request.session.get('email')
        send_otp(email)
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