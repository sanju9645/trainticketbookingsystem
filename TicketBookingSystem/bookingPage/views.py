from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Compartments,Route, Bookings
from profileUpdate.models import Agent
import json
from datetime import datetime


WINDOW = (0,1)
MIDDLE = (2,5)
AISLE = (3,4)

# Create your views here.

def bookingPage(request):
    route_list=Route.objects.all()
    stations = []
    for route in route_list:
        stations.extend(route.route_order.split(','))
    user=request.user
    agent = Agent.objects.filter(user=user)
    if not agent.exists():
        maxSeats = 0
    else:
        maxSeats = agent.last().maxSeats
    
    routes=','.join(stations)
    context={'stations':stations,'maxSeats':maxSeats,'routes':routes}
    return render(request, 'book-ticket.html',context)


def getSeat(window, middle, aisle,gender,priority=AISLE):
    if priority == AISLE:
        seats = aisle + middle + window
    elif priority == MIDDLE:
        seats = middle + aisle + window
    else:
        seats = window + middle + aisle
    if len(seats) <= 0:
        return -1,-1
    
    key = 'female_support'
    if gender=='M':
        key = 'male_support'
    seat=list(filter(lambda x :x[key],seats))
    if len(seat) <= 0:
            return -1,-1
    seat=seat[0]
    return seat, seat['seat_no']%6




def getVacantSeats(journey_start, journey_end, start_date):
    compartment = Compartments.objects.all().last() #last row of compartments
    capacity = compartment.capacity
    train_route = compartment.route.route_order.split(',')
    start_index = train_route.index(journey_start)
    end_index = train_route.index(journey_end)
    journey_route = train_route[start_index: end_index+1]
    
    #all the bookings in this route(start station,end station)
    reserved_seats = Bookings.objects.filter(date_of_journey=start_date.date()).filter(journey_start__in = train_route, journey_end__in = train_route)
    
    # exclude all the bookings that does not affect my booking
    reserved_seats = reserved_seats.exclude(journey_end = journey_start).exclude(journey_start=journey_end)
    seat_structure = [{'seat_no': i+1, 'vacant': True, 'male_support': True, 'female_support': True} for i in range(capacity)]
    
    for seat in reserved_seats:#query set
        index = seat.seat_no-1
        seat_structure[index]['vacant'] = False
        seat_structure[index]['gender'] = seat.passenger_gender
        position = seat.seat_no % 6
        if position in MIDDLE:
            neighbour = (seat.seat_no-1, seat.seat_no+1)
        elif position in (0, 3): # left aisle and right window
            neighbour = (seat.seat_no-1,seat.seat_no-1)
        elif position in (1, 4): # right aisle and left window
            neighbour = (seat.seat_no+1,seat.seat_no+1)
        if seat.passenger_gender == 'M':
            positive_key = 'male_support'
            negative_key = 'female_support'
        else:
            positive_key = 'female_support'
            negative_key = 'male_support'

        seat_structure[neighbour[0]-1][positive_key] = True and seat_structure[neighbour[0]-1][positive_key]
        seat_structure[neighbour[0]-1][negative_key] = False
        seat_structure[neighbour[1]-1][positive_key] = True and seat_structure[neighbour[1]-1][positive_key]
        seat_structure[neighbour[1]-1][negative_key] = False
        
    
    return seat_structure

def allocateSeats(passengers_list, seat_structure):
    senior_citizen = []
    others = []
    for passenger in passengers_list:
        if int(passenger['age']) > 60:
            senior_citizen.append(passenger) 
        else:
            others.append(passenger)
    senior_citizen.sort(key=lambda p: (p['sex'],-int(p['age'])))
    passengers_list = senior_citizen + others

    window_seats = []
    middle_seats = []
    aisle_seats = []
    
    for seat in seat_structure:
        if seat['vacant']==True:
            index = int(seat['seat_no'])%6
            if index in WINDOW:
                window_seats.append(seat)
            elif index in MIDDLE:
                middle_seats.append(seat)
            else:
                aisle_seats.append(seat)
            
    allocated_list = []
    for passenger in passengers_list:
        
        if int(passenger['age'])>60:
            priority = WINDOW
        else:
            priority = AISLE
            
        seat, position = getSeat(window_seats, middle_seats, aisle_seats,passenger['sex'],priority = priority)
        
        if position in WINDOW:
            window_seats.remove(seat)
        elif position in MIDDLE:
            middle_seats.remove(seat)
        elif position in AISLE:
            aisle_seats.remove(seat)
        
        
        if(seat==-1):
            passenger['seat_no']=-1
        else:
            passenger['seat_no']=seat['seat_no']
            
        allocated_list.append(passenger) 
    return allocated_list

@login_required(login_url="/auth/")
def saveBooking(request):
    if request.method != "POST":
        return redirect("ticketBooking")

    booking_details = json.loads(request.body.decode('utf-8'))
    passengers_list = booking_details['passengers']
    journey_start = booking_details['journey_start']
    journey_end = booking_details['journey_end']
    start_date = datetime.strptime(booking_details['start_date'], "%Y-%m-%d")
    seat_structure = getVacantSeats(journey_start, journey_end, start_date)
    booking_result = allocateSeats(passengers_list, seat_structure)
    # save the new bookings 
    for booking in booking_result:
        
        if booking['seat_no'] <= 0:
            continue
        seat_no = booking['seat_no']
        Bookings.objects.create(passenger_name=booking['name'], 
                                passenger_age=booking['age'],
                                passenger_gender=booking['sex'],
                                journey_start=journey_start,
                                journey_end=journey_end,
                                date_of_journey=start_date,
                                seat_no=seat_no)
    context = {}
    return JsonResponse({'status': 1, 'booking_info': booking_result})