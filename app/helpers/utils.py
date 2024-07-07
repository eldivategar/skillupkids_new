from datetime import datetime, timedelta
from app.models import Member, Mitra
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from urllib.parse import quote
from django.utils.html import escape
from django.conf import settings
from django.shortcuts import redirect
from django.conf import settings
import pyotp
import smtplib

def send_otp(request, email):
    
    totp = pyotp.TOTP(pyotp.random_base32(), digits=4, interval=60)
    otp = totp.now()
    
    if 'otp_secret_key' in request.session:
        del request.session['otp_secret_key']
    if 'otp_valid_until' in request.session:
        del request.session['otp_valid_until']
    
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_until'] = str(valid_date)

    receiver_email = email
    subject = 'Kode OTP SkillUpKids'
    messages = f'Gunakan kode berikut untuk masuk ke SkillUpKids. Kode: {otp}'

    try:
        send_mail(
            subject=subject,
            message=messages,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[receiver_email],
            fail_silently=False,
        )        
        return True        
    except Exception as e:
        print(f'Gagal mengirim email: {str(e)}')

def send_email(subject, receiver, context, template_name=['success', 'new_activity']):
    reveiver_email = receiver
    subject = escape(subject)
    
    if template_name == 'success':
        template_message = render_to_string('email_template/success_transaction.html', context)
    else:
        template_message = render_to_string('email_template/new_activity_for_admin_mitra.html', context)
        
    email = EmailMessage(
        subject=subject,
        body=template_message,
        from_email=settings.EMAIL_HOST_USER,
        to=['skillupkidscontact@gmail.com', reveiver_email],        
    )
    email.content_subtype = 'html'
    
    try:
        email.send()
    except Exception as e:
        print(f'Gagal mengirim email: {str(e)}')   

def get_mitra_data(request):
    customer_id = request.session['customer_id']
    uuid = customer_id[2:]
    try:
        data = Mitra.objects.get(uuid=uuid)
        customer_data = {
            'name': data.name,
            'email': data.email,
            'number': data.number,
            'password': data.password,
            'address': data.address,
            'city': data.city,
            'description': data.description,
            'start_time': data.start_time.strftime('%H:%M'),
            'end_time': data.end_time.strftime('%H:%M'),
            'twitter_site': data.twitter_site,
            'fb_site': data.fb_site,
            'ig_site': data.ig_site,
            'linkedin_site': data.linkedin_site,
            'yt_site': data.yt_site,
            'profile_image': data.profile_image,
        }
    except Mitra.DoesNotExist:
        return 'Pengguna tidak ditemukan!'
    
    return customer_data

def get_member_data(request):
    customer_id = request.session['customer_id']
    uuid = customer_id[2:]
    try:
        data = Member.objects.get(uuid=uuid)
        customer_data = {
            'name': data.name,
            'email': data.email,
            'number': data.number,
            'password': data.password,
            'address': data.address,
            'profile_image': data.profile_image,
        }
    except Member.DoesNotExist:
        return 'Pengguna tidak ditemukan!'
    
    return customer_data

def redirect_to_whatsapp(message, number=None):      
    if number == None:
        number = settings.NO_ADMIN
    else:
        if number.startswith('0'):
            number = '+62' + number[1:]        
        
    redirect_to = f'https://api.whatsapp.com/send?phone={number}&text={message}'
    return redirect(redirect_to)