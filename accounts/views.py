from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from .forms import RegistrationForm


def register(request):
    form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    auth_logout(request)  # this clears the session
    return redirect('login')  # redirect to login page after logout