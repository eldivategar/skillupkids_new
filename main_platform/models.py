from django.db import models
from django.contrib.auth.hashers import make_password
import uuid

class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=13, unique=True)
    password = models.CharField(max_length=100)
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
    mitra_id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=13, unique=True)
    password = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField()

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    