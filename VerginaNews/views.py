from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
import categories.models
import articles.models
import authors.models
import urllib.request
import json
import requests
import geoip2.webservice
from decouple import config
from urllib.request import urlopen

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location(ip_address):
    request_url = 'https://geolocation-db.com/jsonp/' + ip_address
    # Send request and decode the result
    response = requests.get(request_url)
    result = response.content.decode()
    # Clean the returned string so it just contains the dictionary data for the IP address
    result = result.split("(")[1].strip(")")
    # Convert this data into a dictionary
    result  = json.loads(result)
    return result['latitude'], result['longitude']

def convert_to_celsius(Fahrenheit):
    Celsius = (Fahrenheit - 32) * 5.0/9.0
    return Celsius

def get_weather(request):
    client_ip = get_client_ip(request)
    lat, lon = get_location('91.184.219.149')
    api=config('WEATHER_API_KEY')

    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={api}'
    weather = requests.get(url).json()

    weather['main']['temp'] = int(convert_to_celsius(weather['main']['temp']))
    weather['icon'] = weather['weather'][0]['icon']
    return weather

class HomepageViews(ListView):
    #context_object_name = 'categories'
    template_name = 'Home.html'
    model = categories.models.Category

    def get(self, request, *args, **kwargs):
        context = {
        'categories_list': categories.models.Category.objects.all(),
        'articles_list': articles.models.Article.objects.all(),
        'authors_list': authors.models.Author.objects.all(),
        'important_list': articles.models.Article.objects.get_important(),
        'roaming_news_list': articles.models.Article.objects.get_latest(),
        'frontnews_list': articles.models.Article.objects.get_frontnews().extra(select={'no_homepage': 'CAST(no_homepage AS INTEGER)'}).order_by('no_homepage'),
        'popular_news_list': articles.models.Article.objects.get_popular(),
        'weather': get_weather(request),
        }
        return render(request, "Home.html", context=context)

    def post(self, request, *args, **kwargs):
        keyword = request.POST.get('search')
        if keyword == "":
            result = 'all'
        else:
            result = keyword
        return redirect('articles_view', search=result)
