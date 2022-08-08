from .utils import get_weather
from django.shortcuts import render, redirect
from .views import HomepageViews

def menu_weather(request):
    menuweather = get_weather(request)
    return dict(menuweather=menuweather)
