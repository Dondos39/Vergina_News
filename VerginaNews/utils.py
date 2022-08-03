from django.core.exceptions import ValidationError
from decouple import config
import requests
import json
import uuid
import os

def image_size_validator(image):
    file_size = image.file.size
    limit_mb = 5
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("Max size of file is %s MB" % limit_mb)

def get_img_path(instance, filename):
    ext = filename.split('.')[-1]
    filename_start = filename.replace('.'+ext,'')
    filename = "%s__%s.%s" % (uuid.uuid4(),filename_start, ext)
    return os.path.join(f'{instance.__class__.__name__}_pics', filename)

def get_video_path(instance, filename):
    ext = filename.split('.')[-1]
    filename_start = filename.replace('.'+ext,'')
    filename = "%s__%s.%s" % (uuid.uuid4(),filename_start, ext)
    return os.path.join('videos', filename)

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
    api=config('WEATHER_API_KEY')
    try:
        lat, lon = get_location('91.184.219.149')
    except requests.exceptions.SSLError:
        lat, lon = (None, None)

    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={api}'
    weather = requests.get(url).json()

    weather['main']['temp'] = int(convert_to_celsius(weather['main']['temp']))
    weather['icon'] = weather['weather'][0]['icon']
    return weather

def get_news(request):
    api=config('NEWS_API_KEY')
    url = f'https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={api}'
    articles = requests.get(url).json()
    return articles['articles']
