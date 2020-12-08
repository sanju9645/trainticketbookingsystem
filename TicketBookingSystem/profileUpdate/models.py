from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Agent(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True,blank=True)
    phone = models.CharField(max_length=200, null=True,blank=True)
    address = models.CharField(max_length=500, null=True,blank=True)
    profile_pic = models.ImageField(null=True, blank=True)
    dob = models.DateField(null=True,blank=True)
    maxSeats = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.user.username