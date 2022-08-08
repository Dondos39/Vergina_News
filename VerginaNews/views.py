from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
import categories.models
import articles.models
import authors.models
import ads.models
import tags.models
import urllib.request
import geoip2.webservice
import datetime
from urllib.request import urlopen
from VerginaNews.utils import get_weather, get_news, get_stocks, get_crypto, get_exchange

class HomepageViews(ListView):
    #context_object_name = 'categories'
    template_name = 'Home.html'
    model = categories.models.Category

    def get(self, request, *args, **kwargs):
        date= datetime.datetime.now()
        context = {
        'categories_list': categories.models.Category.objects.all(),
        'articles_list': articles.models.Article.objects.all(),
        'authors_list': authors.models.Author.objects.get_featured(),
        'important_list': articles.models.Article.objects.get_important(),
        'roaming_news_list': articles.models.Article.objects.get_latest(),
        'frontnews_list': articles.models.Article.objects.get_frontnews().extra(select={'no_homepage': 'CAST(no_homepage AS INTEGER)'}).order_by('no_homepage'),
        'popular_news_list': articles.models.Article.objects.get_popular(),
        'popular_tags': tags.models.Tags.objects.get_popular(),
        'ads': ads.models.Ad.objects.get_priority(1),
        'weather': get_weather(request),
        'external_articles': get_news(request),
        'stocks': get_stocks(request),
        'cryptos': get_crypto(request),
        'forex': get_exchange(request),
        'date': date,
        }
        return render(request, "Home.html", context=context)

    def post(self, request, *args, **kwargs):
        keyword = request.POST.get('search')
        if keyword == "":
            result = 'all'
        else:
            result = keyword
        return redirect('articles_view', search=result)
