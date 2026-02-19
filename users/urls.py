from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
