from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
import json

class Member(models.Model):
    cust_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=13, unique=True)
    password = models.CharField(max_length=100)
    address = models.TextField(default='', null=True, blank=True)
    profile_image = models.ImageField(upload_to='member/', default='member/avatar-profile.jpg', null=True, blank=True)
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
    twitter_site = models.URLField(max_length=200, null=True, blank=True, default='')
    fb_site = models.URLField(max_length=200, null=True, blank=True, default='')
    ig_site = models.URLField(max_length=200, null=True, blank=True, default='')
    linkedin_site = models.URLField(max_length=200, null=True, blank=True, default='')
    yt_site = models.URLField(max_length=200, null=True, blank=True, default='')
    profile_image = models.ImageField(upload_to='mitra/', default='mitra/default-logo.png', null=True, blank=True)
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
    price = models.FloatField()
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

    class Meta:
        verbose_name = 'Kegiatan'
        verbose_name_plural = 'Daftar Kegiatan'
