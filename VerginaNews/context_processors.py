from .views import get_weather

def menu_weather(request):
    menuweather = get_weather(request)
    return dict(menuweather=menuweather)
