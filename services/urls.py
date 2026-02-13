# services/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("services/", views.services_page, name="services"),
    path('booking/', views.booking_page, name='booking'),
    path('contact/', views.contact_page, name='contact'),
    path('booking/history', views.booking_history, name='booking_history'),

]
