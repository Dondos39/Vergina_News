from django.core.exceptions import ValidationError
from decouple import config
import requests
import json
import uuid
import os

def image_size_validator(image):
    file_size = image.file.size
    limit_kb = 200
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)

def get_img_path(instance, filename):
    ext = filename.split('.')[-1]
    filename_start = filename.replace('.'+ext,'')
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(f'{instance.__class__.__name__}_pics', filename)

def get_video_path(instance, filename):
    ext = filename.split('.')[-1]
    filename_start = filename.replace('.'+ext,'')
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('videos', filename)

def get_client_ip(request):
    """Get the IP address of the client.

     Detect the client IP address, then check if it exist and get the ip value
     else return REMOTE_ADDR which is a realable ip address

    Args:
        request : the request object

    Returns:
        ip (string): the ip of the user who made the request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location(ip_address):
    """Get the location of IP address.

     Send request and decode the result. Then clean the returned string so it just contains the
     dictionary data for the IP address and afterwards convert this data into a dictionary.

    Args:
        ip_address (string) : the ip address provided

    Returns:
        lat (float): the latitude of the ip that was provided
        long (float): the longtitude of the ip that was provided
    """
    request_url = 'https://geolocation-db.com/jsonp/' + ip_address

    try:
        response = requests.get(request_url, None, timeout=5)
    except:
        return 37.98, 23.72

    result = response.content.decode()
    result = result.split("(")[1].strip(")")
    try:
        result  = json.loads(result)
    except:
        return 37.98, 23.72
        
    if result['latitude'] != 'Not found' and result['longitude'] != 'Not found':
        return result['latitude'], result['longitude']
    return 37.98, 23.72


def convert_to_celsius(Fahrenheit):
    """Convert Fahrenheit to Celsius.

     Get the temperature provided and convert it to Celsius

    Args:
        Fahrenheit (float) : Temperature in Fahrenheit

    Returns:
        Celsius (int) : Temperature in Celsius
    """
    Celsius = (Fahrenheit - 32) * 5.0/9.0
    return Celsius

def get_weather(request):
    """Get Weather from OpenWeather API.

     Get client ip, then geolocate the ip. Make request using the data provided and get json with data. Convert
     Fahrenheit to Celsius.

    Args:
        request : the request object

    Returns:
        weather (dict) : Weather query.
    """
    client_ip = get_client_ip(request)
    api=config('WEATHER_API_KEY')

    lat, lon = get_location(client_ip)

    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={api}'
    try:
        weather = requests.get(url, None, timeout=5).json()
    except:
        return None

    if weather['cod'] == '400':
        return None

    if weather:
        weather['main']['temp'] = int(convert_to_celsius(weather['main']['temp']))
        weather['icon'] = weather['weather'][0]['icon']
    else:
        return None
    return weather

def get_news(request):
    """Get World News from News API.

     Get JSON from url with API key.

    Args:
        request : the request object

    Returns:
        Articles (dict) : Articles that the json provided.
    """
    api=config('NEWS_API_KEY')
    url = f'https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={api}'
    articles = requests.get(url).json()
    return articles['articles']
