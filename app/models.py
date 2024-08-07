from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from django.utils import timezone
from tinymce.models import HTMLField
from djmoney.models.fields import MoneyField
from babel.numbers import format_currency
import uuid

def format_rupiah(amount):
    return format_currency(amount.amount, 'IDR', locale='id_ID').replace(',00', '').replace('Rp', '').strip()

class Member(models.Model):
    cust_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=13, unique=True)
    password = models.CharField(max_length=100)
    address = models.TextField(default='', null=True, blank=True)
    profile_image = models.ImageField(upload_to='member/', default='member/avatar-profile_n68t05.jpg', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def uuid_str(self):
        return str(self.uuid)
    
    def member_json(self):
        data = {
            'name': self.name,
            'email': self.email,
            'number': self.number,
            'address': self.address,
            'profile_image': self.profile_image,
        }
        return data
    
class Mitra(models.Model):
    mitra_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=13, unique=True)
    password = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=50, default='')
    description = models.TextField()
    start_time = models.TimeField(default='00:00:00')
    end_time = models.TimeField(default='00:00:00')
    twitter_site = models.URLField(max_length=200, blank=True, default='')
    fb_site = models.URLField(max_length=200, blank=True, default='')
    ig_site = models.URLField(max_length=200, blank=True, default='')
    linkedin_site = models.URLField(max_length=200, blank=True, default='')
    yt_site = models.URLField(max_length=200, blank=True, default='')
    profile_image = models.ImageField(upload_to='mitra/', default='mitra/default-logo_sicqfg.png', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def uuid_str(self):
        return str(self.uuid)
    
    def mitra_json(self):
        data = {
            'name': self.name,
            'email': self.email,
            'number': self.number,
            'address': self.address,
            'city': self.city,
            'description': self.description,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'twitter_site': self.twitter_site,
            'fb_site': self.fb_site,
            'ig_site': self.ig_site,
            'linkedin_site': self.linkedin_site,
            'yt_site': self.yt_site,
            'profile_image': self.profile_image,
            'uuid': self.uuid
        }
        return data
    
class ActivityList(models.Model):
    activity_id = models.AutoField(primary_key=True)

    # Basic Information
    activity_name = models.CharField(max_length=100)    
    mitra_activity = models.ForeignKey(Mitra, to_field='uuid', related_name='mitra_activity', on_delete=models.CASCADE)
    category = models.CharField(max_length=50)

    # Activity Information
    day = models.TextField(default='')
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='IDR')
    duration = models.IntegerField(default='')
    age = models.TextField(default='')
    sub_description = models.TextField(default='')
    description = HTMLField(default='')
    learning_method = HTMLField(default='')    

    # Benefit
    benefit = HTMLField(default='', null=True, blank=True)

    # Requirements
    requirements = HTMLField(default='', null=True, blank=True)

    # Additional Information
    additional_information = HTMLField(default='', null=True, blank=True)

    # Activity Image
    activity_image = models.ImageField(upload_to='activity/', default='activity/default-activity.jpg', null=True, blank=True)
    
    # Activity Status
    STATUS = (
        ('pending', 'Pending'),
        ('terbit', 'Terbit'),
        ('ditolak', 'Ditolak'),
    )    
    activity_status = models.CharField(choices=STATUS, max_length=10, default='pending')
    message_status = models.TextField(default='', null=True, blank=True)
        
    def __str__(self):
        return self.activity_name
    
    def full_activity_name(self):
        return f"{self.activity_name} - [{self.mitra_activity.name}]"
    
    def activity_json(self):
        data = {
            'activity_id': self.activity_id,
            'activity_name': self.activity_name,
            'mitra_activity': self.mitra_activity.name,
            'category': self.category,
            'activity_informations': {
                'day': self.day,
                'duration': self.duration,
                'age': self.age,
                'price': format_rupiah(self.price),
                'description': self.description,
                'sub_description': self.sub_description,
                'learning_method': self.learning_method
            },
            'benefit': self.benefit,            
            'requirements': self.requirements,
            'additional_information': self.additional_information,
            'activity_image': self.activity_image,
            'activity_status': {
                'status': self.activity_status,
                'message_status': self.message_status
            }
        }        
        return data        

class Transaction(models.Model):
    transaction_id = models.CharField(primary_key=True, max_length=20, editable=False)
    member = models.ForeignKey(Member, to_field='uuid', related_name='member_transaction', on_delete=models.CASCADE)
    mitra = models.ForeignKey(Mitra, to_field='uuid', related_name='mitra_transaction', on_delete=models.CASCADE)
    activity = models.ForeignKey(ActivityList, to_field='activity_id', related_name='activity_transaction', on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    
    IS_FREE = (
        (True, True),
        (False, False),
    )
    is_free = models.BooleanField(choices=IS_FREE, default=False)
    STATUS = (
        ('Pending', 'Pending'),
        ('Menunggu Pembayaran', 'Menunggu Pembayaran'),
        ('Sukses', 'Sukses'),
        ('Lunas', 'Lunas'),
        ('Gagal', 'Gagal'),
        ('Refund', 'Refund'),
        ('Kadaluwarsa', 'Kadaluwarsa'),
        ('Dibatalkan', 'Dibatalkan'),
    )

    PAYMENT_METHOD = (
        ('Transfer Bank', 'Transfer Bank'),
        ('OVO', 'OVO'),
        ('GoPay', 'GoPay'),
        ('LinkAja', 'LinkAja'),
        ('Dana', 'Dana'),
        ('ShopeePay', 'ShopeePay'),
        ('Alfamart', 'Alfamart'),
        ('Indomaret', 'Indomaret'),     
    )

    status = models.CharField(max_length=50, choices=STATUS, default='Menunggu Pembayaran')
    message_status = models.TextField(default='', blank=True)
    total_price = MoneyField(max_digits=10, decimal_places=2, default_currency='IDR')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD, default='Transfer Bank')
    expired_at = models.DateTimeField(null=True, blank=True, default=None)
    token = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.transaction_id)
    
    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now()

        if not self.is_free and self.expired_at is None:
            self.expired_at = self.date + timezone.timedelta(minutes=60)
        
        super().save(*args, **kwargs)
    
    def transaction_json(self):
        self.check_expired_status()
        if self.is_free or self.status == 'Sukses' or self.status == 'Lunas' or self.status == 'Gagal' or self.status == 'Refund' or self.status == 'Kadaluwarsa' or self.status == 'Dibatalkan':
            data = {
                'transaction_id': self.transaction_id,
                'member': self.member.name,
                'mitra': self.mitra.name,
                'activity_id': self.activity.activity_id,
                'activity': self.activity.activity_name,
                'date': self.date,
                'is_free': self.is_free,
                'status': self.status,
                'total_price': format_rupiah(self.total_price),
                'payment_method': self.payment_method,                            
            }

        else:
            data = {
                    'transaction_id': self.transaction_id,
                    'member': self.member.name,
                    'mitra': self.mitra.name,
                    'activity': self.activity.activity_name,
                    'date': self.date,
                    'is_free': self.is_free,
                    'status': self.status,
                    'total_price': format_rupiah(self.total_price),
                    'payment_method': self.payment_method,
                    'expired_at': self.expired_at,
                    'token': self.token
                }
        return data
    
    def check_expired_status(self):
        if self.status == 'Menunggu Pembayaran' and timezone.now() > self.expired_at:
            self.status = 'Gagal'
            self.save()

def generate_transaction_id():
    tahun_sekarang = datetime.now().year
    angka_unik = uuid.uuid4().int & (1<<64)-1
    return f'SUK-{tahun_sekarang}-{angka_unik:013d}'[:20]

class Testimonial(models.Model):
    testimonial_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, to_field='uuid', related_name='member_testimonial', on_delete=models.CASCADE)
    # mitra = models.ForeignKey(Mitra, to_field='uuid', related_name='mitra_testimonial', on_delete=models.CASCADE)
    activity = models.ForeignKey(ActivityList, to_field='activity_id', related_name='activity_testimonial', on_delete=models.CASCADE)
    testimonial = models.TextField(default='')
    rating = models.IntegerField(default=0, 
                                 validators=[
                                    MaxValueValidator(5),
                                    MinValueValidator(0)
                                 ])
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.testimonial
    
    def testimonial_json(self):
        data = {
            'testimonial_id': self.testimonial_id,
            'member': self.member.name,
            'mitra': self.activity.mitra_activity.name,
            'activity': self.activity.activity_name,
            'testimonial': self.testimonial,
            'rating': self.rating,
            'date': self.date
        }
        return data

class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    content = HTMLField(null=True, blank=True)
    image = models.ImageField(upload_to='blog/', default='blog/default-blog.jpg', null=True, blank=True)
    tag = models.CharField(max_length=50, default='')
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def blog_json(self):
        data = {
            'blog_id': self.blog_id,
            'title': self.title,
            'content': self.content,
            'image': self.image,
            'tag': self.tag,
            'created_at': self.created_at
        }
        return data
    
class FeaturedActivity(models.Model):
    activity = models.OneToOneField(ActivityList, on_delete=models.CASCADE)

    def __str__(self):
        return self.activity.activity_name
    
    def featured_activity_json(self):
        data = {
            'activity_id': self.activity.activity_id,
            'activity_name': self.activity.activity_name,
            'mitra_activity': {
                'name': self.activity.mitra_activity.name,
                'profile_image': self.activity.mitra_activity.profile_image,
                },
            'category': self.activity.category,
            'activity_informations': {
                'day': self.activity.day,
                'duration': self.activity.duration,
                'age': self.activity.age,
                'price': format_rupiah(self.activity.price),
                'description': self.activity.description,
                'sub_description': self.activity.sub_description,
                'learning_method': self.activity.learning_method
            },
            'benefit': self.activity.benefit,            
            'requirements': self.activity.requirements,
            'additional_information': self.activity.additional_information,
            'activity_image': self.activity.activity_image,
            'activity_status': {
                'status': self.activity.activity_status,
                'message_status': self.activity.message_status
            }
        }        
        return data
    
class OTP(models.Model):
    code = models.CharField(max_length=4)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    @staticmethod
    def generate_code():
        return str(uuid.uuid4().int)[:4]

    def is_valid(self):
        return datetime.now() < self.expires_at