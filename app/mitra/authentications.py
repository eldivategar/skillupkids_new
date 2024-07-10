from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from app.helpers.decorators import is_registering
from app.models import Mitra
from app.helpers.utils import send_otp, verify_otp

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
            
            request.session['name'] = name
            request.session['email'] = email
            request.session['number'] = number
            request.session['password'] = password
            request.session['is_registering'] = True

            if send_otp(email):
                messages.success(request, 'Kode berhasil dikirim ke email anda!')
                return redirect('app.mitra:verify')
            else:
                messages.error(request, 'Gagal mengirim kode OTP, Coba beberapa saat lagi!')
                return redirect('app.mitra:register')

@is_registering
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

@is_registering
def verify_account(request):
    
    if request.method == 'GET':        
        return render(request, 'mitra/auth/verify.html')

    if request.method == 'POST':
        user_otp = ''.join([request.POST.get(f'digit-{i}') for i in range(1, 5)])
        email = request.session['email']

        if verify_otp(email, user_otp):
            name = request.session['name']
            email = request.session['email']
            number = request.session['number']
            password = request.session['password']
            
            mitra = Mitra(name=name, email=email, number=number, password=password, is_verified=True)
            mitra.save()
            
            customer_uuid = f'mi{mitra.uuid_str()}'
            request.session['customer_id'] = customer_uuid
            
            return redirect('app.mitra:register_2')
                
        else:
            messages.error(request, 'Kode OTP salah atau sudah kadaluarsa!')
            return redirect('app.mitra:verify')
        
@is_registering
def resend_code(request):
    if request.method == 'GET':
        email = request.session.get('email')
        send_otp(email)
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