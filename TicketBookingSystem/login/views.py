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
# Create your views here.

@login_required(login_url="/auth/")
def home(request):
    context = {}
    agent = Agent.objects.filter(user=request.user)
    if agent.exists():
        agent = agent.last()
        if None in [agent.name, agent.phone, agent.dob, agent.address, agent.profile_pic]:
            return redirect("updateProfile")
        compartment = Compartments.objects.filter()
        if compartment.exists():
            capacity = compartment.last().capacity
            bookings = Bookings.objects.all()
            date_str = datetime.today().strftime("%Y-%m-%d")
            if request.method == "POST":
                date_str = request.POST.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d')
            bookings = bookings.filter(date_of_journey=date)
            seats = []
            for seat_no in range(1, capacity+1):
                reserv = bookings.filter(seat_no=seat_no)
                passenger = []
                if reserv.exists():
                    color = '#ffffff'
                    for r in reserv:
                        c = '#4287f5' if reserv.last().passenger_gender=='M' else '#f542b9'
                        passenger.append({'start': r.journey_start, 'end': r.journey_end, 'color': c})
                else:
                    color = '#e6e6e6'
                seats.append({'passengers': passenger, 'vacant': len(passenger)==0, 'color': color})
            context['capacity'] =  capacity
            context['seats'] = seats
            context['booking_date'] = date_str
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
    reset_url = f'{settings.CURRENT_HOST}{reset_path}'
    return reset_url