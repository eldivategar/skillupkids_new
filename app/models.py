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
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def uuid_str(self):
        return str(self.uuid)
    
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
    twitter_site = models.URLField(max_length=200, null=True, default='')
    fb_site = models.URLField(max_length=200, null=True, default='')
    ig_site = models.URLField(max_length=200, null=True, default='')
    linkedin_site = models.URLField(max_length=200, null=True, default='')
    yt_site = models.URLField(max_length=200, null=True, default='')
    profile_image = models.ImageField(upload_to='mitra/', default='mitra/default-logo.png', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def uuid_str(self):
        return str(self.uuid)
    
class ActivityList(models.Model):
    activity_id = models.AutoField(primary_key=True)

    # Basic Information
    activity_name = models.CharField(max_length=100)    
    mitra_activity = models.ForeignKey(Mitra, to_field='uuid', related_name='mitra_activity', on_delete=models.CASCADE)
    category = models.CharField(max_length=50)

    # Activity Information
    day = models.TextField(default='')
    price = models.IntegerField()
    duration = models.IntegerField(default='')
    age = models.TextField(default='')
    description = models.TextField()
    learning_method = models.TextField(default='')    

    # Benefit
    benefit = models.TextField()

    # Requirements
    requirements = models.TextField(default='')

    # Additional Information
    additional_information = models.TextField(default='')

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
                'description': self.description,
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
