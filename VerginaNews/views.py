from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
import categories.models
import articles.models

class HomepageViews(ListView):
    #context_object_name = 'categories'
    template_name = 'Home.html'
    model = categories.models.Category

    def get_context_data(self, **kwargs):
        context = super(HomepageViews, self).get_context_data(**kwargs)
        context.update({
            'categories_list': categories.models.Category.objects.all(),
            'important_list': articles.models.Article.objects.get_important().values('id', 'no_important', 'title'),
            'roaming_news_list': articles.models.Article.objects.get_latest(),
            'frontnews_list': articles.models.Article.objects.get_frontnews().order_by('no_homepage'),
            
        })
        print(context['important_list'])
        return context
  
