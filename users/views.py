from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('landing')  
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

#code below limit number of login attempts to 5 times to reduce brute force attacks
MAX_ATTEMPTS = 5
LOCK_TIME = 1800  # 30 minutes (seconds)


def custom_login(request):
    
   form = AuthenticationForm(request, data=request.POST or None)
       
   if request.method == "POST":
        username = request.POST.get("username")
       # password = request.POST.get("password")

        lock_key = f"lock_{username}"
        attempts_key = f"attempts_{username}"

        # Checks if account is locked
        lock_time = cache.get(lock_key)
        if lock_time:
            remaining = int((lock_time - timezone.now()).total_seconds() / 60)
            messages.error(
                request,
                f"Account locked. Try again in {remaining} minutes."
            )
            return render(request, "users/login.html")

     
        else:
            attempts = cache.get(attempts_key, 0) + 1
            cache.set(attempts_key, attempts, timeout=LOCK_TIME)

            if attempts >= MAX_ATTEMPTS:
                lock_until = timezone.now() + timedelta(seconds=LOCK_TIME)
                cache.set(lock_key, lock_until, timeout=LOCK_TIME)
                messages.error(
                    request,
                    "Too many failed attempts. Account locked for 30 minutes."
                )
            else:
                messages.error(
                    request,
                    f"Invalid credentials. Attempt {attempts}/{MAX_ATTEMPTS}"
                )

        return render(request, "users/login.html", {"form": form})

#the code below was only perfoming normal authentication 
"""def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('landing')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})"""


def logout_view(request):
    logout(request)
    return redirect('landing')

