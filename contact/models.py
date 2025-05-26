from django.db import models

# Create your models here.

class Contact(models.Model):
    full_name=models.CharField(max_length=50)
    email=models.CharField(max_length=60)
    phone=models.CharField(max_length=10)
    address=models.CharField(max_length=400)
    country=models.CharField(max_length=15)
    state=models.CharField(max_length=15)
    city=models.CharField(max_length=15)
    pincode=models.CharField(max_length=10)
    message=models.TextField() 

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email