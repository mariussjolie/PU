"""Module containing endpoints for login/signup"""
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from WebApp.auth.user_register_form import UserRegisterForm


def signup(request):
    """Signup endpoint"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/signup.html', {'form': form})
