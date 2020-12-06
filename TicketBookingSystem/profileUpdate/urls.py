from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profile/', views.showProfilePage, name="showProfile"),
    path('profile/update/', views.updateProfilePage, name="updateProfile"),
]