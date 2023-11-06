from django.db import models
from django.contrib.auth.hashers import make_password
import uuid

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
    twitter_site = models.URLField(max_length=200, null=True)
    fb_site = models.URLField(max_length=200, null=True)
    ig_site = models.URLField(max_length=200, null=True)
    linkedin_site = models.URLField(max_length=200, null=True)
    yt_site = models.URLField(max_length=200, null=True)
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
    