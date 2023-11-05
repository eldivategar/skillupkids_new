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
        if 'customer_id' in request.session:
            return redirect('app.mitra:mitra_profile')
        else:
            return render(request, 'mitra/auth/login.html')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            mitra = Mitra.objects.filter(email=email).first()

            if mitra:
                if check_password(password, mitra.password):
                    request.session['customer_id'] = mitra.uuid_str()
                    request.session['user_type'] = 'mitra'
                    return redirect('app.mitra:mitra_profile')
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

        customer = Mitra.objects.get(uuid=request.session['customer_uuid'])
        customer.city = city
        customer.address = address
        customer.description = description
        customer.start_time = start_time    
        customer.end_time = end_time
        customer.twitter_site = twitter_site
        customer.fb_site = fb_site
        customer.ig_site = ig_site
        customer.linkedin_site = linkedin_site
        customer.yt_site = yt_site
        customer.profile_image.save(logo.name, logo, save=True)
        customer.save()

        request.session.flush()
        request.session['customer_id'] = customer.uuid_str()
        request.session['user_type'] = 'mitra'
        return redirect('app.mitra:mitra_profile')         

@user_must_be_registered
def verify_account(request):
    
    if request.method == 'GET':        
        return render(request, 'mitra/auth/verify.html')

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

                    customer = Mitra(name=name, email=email, number=number, password=password, is_verified=True)
                    customer.save()

                    request.session.flush()
                    import uuid
                    unique_code = str(uuid.uuid4())
                    request.session['unique_code'] = unique_code
                    request.session['customer_uuid'] = customer.uuid_str()
                    
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
        email = request.session['email']
        send_otp(request, email)
        messages.success(request, 'Kode berhasil dikirim ke email anda!')
        return redirect('app.mitra:verify')