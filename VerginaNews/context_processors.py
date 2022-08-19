from .utils import get_weather
from django.shortcuts import render, redirect
from .views import HomepageViews
from django.core.validators import validate_email
from django import forms
from django.contrib import messages
from subscribers.models import Subscriber

def menu_weather(request):
    menuweather = get_weather(request)
    return dict(menuweather=menuweather)

def subscribe(request):
    message = None
    if 'email' in request.session:
        email = request.session['email']
        del request.session['email']

        if email != None:
            try:
                validate_email(email)
            except forms.ValidationError:
                message = 'Please enter a correct email address.'
            else:
                if Subscriber.objects.filter(email=email).exists():
                    message = 'Email Address already exists.'
                else:
                    message = 'Subscribed succesfully.'
                    sub = Subscriber(email=email)
                    sub.save()

    return dict(message=message)
