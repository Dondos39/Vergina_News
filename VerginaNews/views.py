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
import time
from urllib.request import urlopen
from VerginaNews.utils import get_weather, get_news
from django.core.paginator import Paginator


class HomepageViews(ListView):
    #context_object_name = 'categories'
    template_name = 'Home.html'
    model = categories.models.Category

    def get(self, request, *args, **kwargs):
        category = categories.models.Category.objects.only('name')
        paginator = Paginator(category, 1)
        page = request.GET.get('page')
        page_category = paginator.get_page(page)
        category_count = len(category)
        date= datetime.datetime.now()

        context = {
        'categories_list': page_category,
        'categories_count': category_count,
        'authors_list': authors.models.Author.objects.get_featured(),
        'important_list': articles.models.Article.objects.get_important(),
        'roaming_news_list': articles.models.Article.objects.get_latest(),
        'frontnews_list': articles.models.Article.objects.get_frontnews().extra(select={'no_homepage': 'CAST(no_homepage AS INTEGER)'}).order_by('no_homepage'),
        'popular_news_list': articles.models.Article.objects.get_popular(),
        'popular_tags': tags.models.TagCloud.get_tags,
        'ad_banner_1': ads.models.get_priority(1),
        'ad_banner_2': ads.models.get_priority(6),
        'ad_news_1': ads.models.get_priority(2),
        'ad_news_2': ads.models.get_priority(3),
        'ad_news_3': ads.models.get_priority(4),
        'ad_news_4': ads.models.get_priority(5),
        'weather': get_weather(request),
        'external_articles': get_news(request),
        'date': date,
        }
        return render(request, "Home.html", context=context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('ad_id'):
            id = request.POST.get('ad_id')
            ad = ads.models.Ad.objects.get(id=id)
            ad.total_views = ad.total_views + 1
            ad.save(update_fields=['total_views'])
            return HttpResponseRedirect(ad.url)

        keyword = request.POST.get('search')
        if keyword == "":
            result = 'all'
        else:
            result = keyword
        return redirect('articles_view', search=result)
