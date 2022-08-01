from .views import get_weather

def menu_weather(request):
    menuweather = get_weather(request)
    print("_______________________")
    print(menuweather)
    return dict(menuweather=menuweather)