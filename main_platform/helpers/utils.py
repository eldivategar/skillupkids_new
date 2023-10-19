from datetime import datetime, timedelta
import pyotp
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_otp(request, email):
    
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
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

