from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django import utils
from TicketBookingSystem import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from profileUpdate.models import Agent
from bookingPage.models import Compartments, Bookings
from datetime import datetime

    # using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
#from sendgrid import SendGridAPIClient
#from sendgrid.helpers.mail import Mail
# Create your views here.

#if the request is not autherized it will reidrect to auth page
@login_required(login_url="/auth/")#1st parameter home,2nd login_url
def home(request):
    context = {}
    agent = Agent.objects.filter(user=request.user)#filter returns a queryset
    if agent.exists():
        agent = agent.last() #to get last object of queryset agent
        if None in [agent.name, agent.phone, agent.dob, agent.address, agent.profile_pic]:
            return redirect("updateProfile")
        compartment = Compartments.objects.filter()
        if compartment.exists():
            capacity = compartment.last().capacity
            bookings = Bookings.objects.all()
            date_str = datetime.today().strftime("%Y-%m-%d")#datetime.today() return today date
            #strftime()-string formate time converts date object to string
            if request.method == "POST" :
                date_str = request.POST.get('date')
                
            date = datetime.strptime(date_str, '%Y-%m-%d')
            #strptime()-string parsee time converts string to date object
            
            bookings = bookings.filter(date_of_journey=date)
            seats = []
            for seat_no in range(1, capacity+1):
                reserv = bookings.filter(seat_no=seat_no)
                passenger = []
                if reserv.exists():
                    color = '#ffffff'
                    for r in reserv:
                        c = '#4287f5' if r.passenger_gender=='M' else '#f542b9'
                        passenger.append({'start': r.journey_start, 'end': r.journey_end, 'color': c})
                else:
                    color = '#e6e6e6'
                    
                seats.append({'passengers': passenger, 'vacant': len(passenger)==0, 'color': color})

            context['capacity'] =  capacity
            context['seats'] = seats
            context['booking_date'] = date_str # to prevent the form becoming empty after submitting.This will send the datewith each response
    return render(request, "home.html", context)

def login_user(request):
    return render(request,'index.html', {})

def signout(request):
    logout(request)
    return redirect('/?message=Succesfully Logged Out')

def signin(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        user = authenticate(username=email,password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('/auth/?message=Invalid Credentials ! ! !')
    return redirect('/auth/')


def get_password_reset_url(user):
    base64_encoded_id = utils.http.urlsafe_base64_encode(utils.encoding.force_bytes(user.id))
    token = PasswordResetTokenGenerator().make_token(user)
    reset_url_args = {'uidb64': base64_encoded_id, 'token': token}
    reset_path = reverse('password_reset_confirm', kwargs=reset_url_args)
    #reset_url = f'{settings.CURRENT_HOST}{reset_path}'
    reset_url = 'https://trainticketbookingsystem.herokuapp.com'+reset_path
    return reset_url


# def send_mail(subject,message,to):
#     message = Mail(
#         from_email='bookyourticketsapp@gmail.com',
#         to_emails=to,
#         subject=subject,
#         html_content=message)
#     try:
#         sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#         response = sg.send(message)
#         print(response.status_code)
#         print(response.body)
#         print(response.headers)
#     except Exception as e:
#         print(e)