from datetime import datetime, timedelta
from app.models import Member, Mitra
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pyotp
import smtplib

def send_otp(request, email):
    
    totp = pyotp.TOTP(pyotp.random_base32(), digits=4, interval=60)
    otp = totp.now()
    
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_until'] = str(valid_date)

    sender_email = 'skillupkidscontact@gmail.com'
    sender_password = 'yfmv ljvd vfga fyab'
    receiver_email = email
    subjek_email = 'Kode OTP SkillUpKids'
    messages = f'Gunakan kode berikut untuk masuk ke SkillUpKids. Kode: {otp}'

    pesan = MIMEMultipart()
    pesan['From'] = sender_email
    pesan['To'] = receiver_email
    pesan['Subject'] = subjek_email
    pesan.attach(MIMEText(messages, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, pesan.as_string())
        server.quit()
        # print('Email terkirim dengan sukses')
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