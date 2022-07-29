from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
import categories.models
import articles.models
import authors.models
import urllib.request
import json
from decouple import config

def get_weather():
    api=config('WEATHER_API_KEY')
    print('--------------')
    print(api)
    print('--------------')

    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&units=imperial&appid={api}'
    weather = request.get(url).json()

    print('--------------')
    print(weather)
    print('--------------')

    context = {'weather' : weather}

    return render(request, 'weather/index.html', context)

class HomepageViews(ListView):
    #context_object_name = 'categories'
    template_name = 'Home.html'
    model = categories.models.Category

    def get_context_data(self, **kwargs):
        context = super(HomepageViews, self).get_context_data(**kwargs)
        context.update({
            'categories_list': categories.models.Category.objects.all(),
            'articles_list': articles.models.Article.objects.all(),
            'authors_list': authors.models.Author.objects.all(),
            'important_list': articles.models.Article.objects.get_important(),
            'roaming_news_list': articles.models.Article.objects.get_latest(),
            'frontnews_list': articles.models.Article.objects.get_frontnews().extra(select={'no_homepage': 'CAST(no_homepage AS INTEGER)'}).order_by('no_homepage'),
            'popular_news_list': articles.models.Article.objects.get_popular(),
            'weather': get_weather(),
        })

        return context

    def post(self, request, *args, **kwargs):
        keyword = request.POST.get('search')
        if keyword == "":
            result = 'all'
        else:
            result = keyword
        return redirect('articles_view', search=result)
