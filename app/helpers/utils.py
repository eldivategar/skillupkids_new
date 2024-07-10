from datetime import datetime, timedelta
from app.models import Member, Mitra, OTP
from datetime import datetime
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.html import escape
from django.shortcuts import redirect
from django.conf import settings

def send_otp(email):
    otp_code = OTP.generate_code()
    expiration_time = datetime.now() + timedelta(minutes=5)

    OTP.objects.create(
        code=otp_code,
        email=email,
        expires_at=expiration_time
    )

    subject = 'Kode OTP SkillUpKids'
    message = f'Gunakan kode berikut untuk masuk ke SkillUpKids. Kode: {otp_code}'

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f'Gagal mengirim email: {str(e)}')
        return False

def verify_otp(email, user_otp):
    try:
        otp_record = OTP.objects.filter(email=email).latest('created_at')
        if otp_record.is_valid() and otp_record.code == user_otp:
            return True
    except OTP.DoesNotExist:
        pass
    return False

def send_email(subject, receiver, context, template_name=['success', 'new_activity']):
    receiver_email = receiver
    subject = escape(subject)
    
    if template_name == 'success':
        template_message = render_to_string('email_template/success_transaction.html', context)
        to = [receiver_email]
    else:
        template_message = render_to_string('email_template/new_activity_for_admin_mitra.html', context)
        to = ['skillupkidscontact@gmail.com', receiver_email]
        
    email = EmailMessage(
        subject=subject,
        body=template_message,
        from_email=settings.EMAIL_HOST_USER,
        to=to
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