from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from app.helpers.decorators import user_must_be_registered
from app.models import Mitra
from app.helpers.utils import send_otp
from datetime import datetime
import pyotp

def login(request):
    if request.method == 'GET':        
        return render(request, 'mitra/auth/login.html')
    
    if request.method == 'POST':
        request.session.flush()
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            mitra = Mitra.objects.filter(email=email).first()

            if mitra:
                if check_password(password, mitra.password):
                    customer_uuid = f'mi{mitra.uuid_str()}'
                    request.session['customer_id'] = customer_uuid
                    return redirect('app.mitra:mitra_dashboard_activity_list')
                else:
                    messages.error(request, 'Ups, Password salah!')
                    return redirect('app.mitra:login')
                                
            else: 
                messages.error(request, 'Email belum terdaftar di SkillUpKids!')
                return redirect('app.mitra:login')

def register(request):
    if request.method == 'GET':
        return render(request, 'mitra/auth/register-1.html')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('num_wa')
        password = request.POST.get('password')
        
        if email and number:
            if Mitra.objects.filter(email=email).exists():
                messages.error(request, 'Email sudah terdaftar!')
                return redirect('app.mitra:register')
                        
            if Mitra.objects.filter(number=number).exists():
                messages.error(request, 'Nomor whatsapp sudah terdaftar!')
                return redirect('app.mitra:register')
                        
            import uuid
            unique_code = str(uuid.uuid4())
            request.session['unique_code'] = unique_code 
            
            request.session['name'] = name
            request.session['email'] = email
            request.session['number'] = number
            request.session['password'] = password
            # request.session.set_expiry(400)

            send_otp(request, email)          
            messages.success(request, 'Kode berhasil dikirim ke email anda!')

            return redirect('app.mitra:verify')
        else:
            return redirect('app.mitra:register')

@user_must_be_registered
def register_2(request):
    if request.method == 'GET':
        return render(request, 'mitra/auth/register-2.html')
    
    if request.method == 'POST':
        city = request.POST.get('city')
        address = request.POST.get('address')
        description = request.POST.get('description')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        twitter_site = request.POST.get('twitter_site')
        fb_site = request.POST.get('fb_site')
        ig_site = request.POST.get('ig_site')
        linkedin_site = request.POST.get('linkedin_site')
        yt_site = request.POST.get('yt_site')                
        logo = request.FILES.get('logo')

        uuid = request.session.get('customer_id')[2:]
        mitra = Mitra.objects.get(uuid=uuid)
        mitra.city = city
        mitra.address = address
        mitra.description = description
        mitra.start_time = start_time    
        mitra.end_time = end_time
        mitra.twitter_site = twitter_site
        mitra.fb_site = fb_site
        mitra.ig_site = ig_site
        mitra.linkedin_site = linkedin_site
        mitra.yt_site = yt_site
        
        if logo:
            mitra.profile_image.save(logo.name, logo, save=True)
        
        mitra.save()

        request.session.flush()
        customer_uuid = f'mi{mitra.uuid_str()}'
        request.session['customer_id'] = customer_uuid
        return redirect('app.mitra:mitra_profile')         

@user_must_be_registered
def verify_account(request):
    
    if request.method == 'GET':        
        return render(request, 'mitra/auth/verify.html')

    if request.method == 'POST':
        user_otp = request.POST.get('digit-1') + request.POST.get('digit-2') + request.POST.get('digit-3') + request.POST.get('digit-4')
        user_otp = int(user_otp)
        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_until = request.session.get('otp_valid_until')

        if otp_secret_key is not None and otp_valid_until is not None:
            valid_until = datetime.fromisoformat(otp_valid_until)
            if valid_until > datetime.now():                
                totp = pyotp.TOTP(otp_secret_key, digits=4, interval=60)

                if totp.verify(user_otp):

                    name = request.session.get('name')
                    email = request.session.get('email')
                    number = request.session.get('number')
                    password = request.session.get('password')

                    mitra = Mitra(name=name, email=email, number=number, password=password, is_verified=True)
                    mitra.save()

                    customer_uuid = f'mi{mitra.uuid_str()}'
                    request.session['customer_id'] = customer_uuid
                    
                    return redirect('app.mitra:register_2')
                
                else:
                    messages.error(request, 'Kode OTP salah!')
                    return redirect('app.mitra:verify')
            
            else:
                messages.error(request, 'Kode OTP sudah kadaluarsa!')
                return redirect('app.mitra:verify')

        else:
            messages.error(request, 'Ups...terjadi kesalahan, silahkan coba lagi!')
            return redirect('app.mitra:verify')
        
@user_must_be_registered
def resend_code(request):
    if request.method == 'GET':
        email = request.session.get('email')
        send_otp(request, email)
        messages.success(request, 'Kode berhasil dikirim ke email anda!')
        return redirect('app.mitra:verify')

def forgot_password(request):
    if request.method == 'GET':
        return render(request, 'mitra/auth/forgot-password.html')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if email:
            if Mitra.objects.filter(email=email).exists():
                if password == confirm_password:
                    mitra = Mitra.objects.get(email=email)
                    mitra.password = password
                    mitra.save()
                    messages.success(request, 'Password berhasil diubah!')
                    return redirect('app.mitra:login')
                else:
                    messages.error(request, 'Password tidak sama!')                
                return redirect('app.mitra:forgot_password')
            else:
                messages.error(request, 'Email belum terdaftar!')
                return redirect('app.mitra:forgot_password')
        else:
            messages.error(request, 'Ups...terjadi kesalahan, silahkan coba lagi!')
            return redirect('app.mitra:forgot_password')