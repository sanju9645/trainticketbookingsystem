from django.urls import path
from django.views.generic import TemplateView


from . import views

urlpatterns = [
    path('tickets/',views.bookingPage,name='ticketBooking'),
    path('save/', views.saveBooking, name="saveBooking"),
]