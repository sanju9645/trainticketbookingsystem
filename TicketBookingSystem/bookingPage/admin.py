from django.contrib import admin

# Register your models here.
from .models import Route,Compartments,Bookings

admin.site.register(Route)
admin.site.register(Compartments)
admin.site.register(Bookings)