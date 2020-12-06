from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Agent(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=500, null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    dob = models.DateTimeField(auto_now_add=True, null=True)
    maxSeats = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.user.username