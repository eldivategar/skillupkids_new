from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from django.utils import timezone
import uuid

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
    price = models.DecimalField(max_digits=10, decimal_places=3, default='')
    duration = models.IntegerField(default='')
    age = models.TextField(default='')
    description = models.TextField(default='')
    sub_description = models.TextField(default='')
    learning_method = models.TextField(default='')    

    # Benefit
    benefit = models.TextField(default='', null=True, blank=True)

    # Requirements
    requirements = models.TextField(default='', null=True, blank=True)

    # Additional Information
    additional_information = models.TextField(default='', null=True, blank=True)

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
                'price': self.price,
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

class Testimonial(models.Model):
    testimonial_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, to_field='uuid', related_name='member_testimonial', on_delete=models.CASCADE)
    # mitra = models.ForeignKey(Mitra, to_field='uuid', related_name='mitra_testimonial', on_delete=models.CASCADE)
    activity = models.ForeignKey(ActivityList, to_field='activity_id', related_name='activity_testimonial', on_delete=models.CASCADE)
    testimonial = models.TextField(default='')
    rating = models.IntegerField(default=0)
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
    total_price = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD, default='Transfer Bank')
    expired_at = models.DateTimeField(null=True, blank=True, default=None)
    token = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.transaction_id)
    
    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now()

        if not self.is_free and self.expired_at is None:
            self.expired_at = self.date + timezone.timedelta(minutes=10)
        
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
                'total_price': self.total_price,
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
                    'total_price': self.total_price,
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


# @receiver(pre_save, sender=Transaction)
# def set_transaction_id(sender, instance, **kwargs):
#     # if not instance.transaction_id:
#     #     instance.transaction_id = generate_transaction_id()
    
#     if not instance.date:
#         instance.date = timezone.now()