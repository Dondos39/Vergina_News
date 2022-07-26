from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
import categories.models
import articles.models
import authors.models


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
        })
        return context
