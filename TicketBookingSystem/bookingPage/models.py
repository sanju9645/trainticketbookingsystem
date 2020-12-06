from django.db import models

# Create your models here.

class Route(models.Model):
    route_order = models.CharField(max_length=200, null=False, blank=False) 
    # comma separated string of stations in the route in the order of journey

    def ___str__(self):
        return self.route_order


class Compartments(models.Model):
    route = models.ForeignKey(Route, null=False, blank=False, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Train No. {self.id} Capacity: {self.capacity}"


class Bookings(models.Model):
    gender_choices = (
        ("F", "F"),
        ("M", "M")
    )
    passenger_name = models.CharField(max_length=200, null=False, blank=False)
    passenger_age = models.PositiveIntegerField(null=False, blank=False)
    passenger_gender = models.CharField(max_length=1, null=False, blank=False, choices=gender_choices)
    journey_start = models.CharField(max_length=10, null=False, blank=False)
    journey_end = models.CharField(max_length=10, null=False, blank=False)
    date_of_journey = models.DateTimeField(null=False, blank=False)
    seat_no = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.seat_no}   {self.passenger_name} {self.passenger_gender}   {self.journey_start} {self.journey_end}  {self.date_of_journey.date()} "