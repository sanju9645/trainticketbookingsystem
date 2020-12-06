from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from TicketBookingSystem import settings
from .views import *
from profileUpdate.models import *

import os
import requests
from django.dispatch import receiver
from login.views import send_mail


@receiver(post_save,sender=User)
def hear_signal(sender,instance,**kwargs):
    #kwrgs   keyword argument
    if kwargs.get('created'):
        # create correspondng Agent model
        a = Agent.objects.create(user=instance)
        if a:
            print("Agent creation successful")
        else:
            print("Agent creation failed")
        # Send verification mail
        subject='Account activation mail'
        message='Congatulations,\n Your account is activated.\nPlease login from this link to continue\n  ' + get_password_reset_url(instance)
        #response = send_simple_message(instance.username, subject, message)
        #print(response.status_code, response.text)
        send_mail(subject, 
                message, 
                instance.username)

# def send_simple_message(to, subject, message):
# 	return requests.post(
# 		"https://api.mailgun.net/v3/sandboxd214269ab7104244ba9fcf2aebdcae12.mailgun.org/messages",
# 		auth=("api", "7334fb874bad9c9d5513229df468bbf1-95f6ca46-6726ee2e"),
# 		data={"from": "Mailgun Sandbox <postmaster@sandboxd214269ab7104244ba9fcf2aebdcae12.mailgun.org>",
# 			"to": to,
# 			"subject": subject,
# 			"text": message})

