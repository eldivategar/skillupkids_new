from django.db import models

class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=13, unique=True)
    password = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name
    
class Mitra(models.Model):
    mitra_id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=13, unique=True)
    password = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField()
    
    def __str__(self):
        return self.name
    