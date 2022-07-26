from django.shortcuts import render
from .models import Article
from categories.models import SubCategory
import articles.models
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
# import requests

# Create your views here.
def get_subcategory(request):
    id = request.GET.get('id', '')
    result = list(SubCategory.objects.filter(
    category_id=int(id)).values('id', 'name'))
    return HttpResponse(json.dumps(result), content_type="application/json")

# def newshome(request):
#     news_api_request = requests.get("https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=d9051363b5064c83a6c6983704369199")
#     api = json.load(news_api_request)
#     return render (request, 'Home.html', {'api':api})

class ArticleView(DetailView):
        context_object_name = 'articles'
        template_name = 'article.html'
        model = articles.models.Article

        def get(self, request, *args, **kwargs):
            post_id = self.kwargs.get('post_id')

            detail = articles.models.Article.objects.get(id=post_id)
            context = {
            "id": detail.id,
            "title": detail.title,
            "authors": detail.get_authors(),
            "updated_at":detail.updated_at,
            "comments": detail.get_comments(),
            "category": detail.category.name,
            "sub_category": detail.sub_category.name,
            "related_articles": articles.models.Article.objects.filter(category=detail.category, sub_category=detail.sub_category).exclude(id=detail.id)
            }
            return render(request, "article.html", context=context)

        def post(self, request, *args, **kwargs):
            id = request.POST.get('Article ID')
            article = articles.models.Article.objects.get(id=id)
            comment = {
            "author": request.POST.get('author'),
            "email": request.POST.get('email'),
            "text": request.POST.get('comment')
            }

            article.add_comment(comment)
            context = {
            'post_id': article.id,
            'category': article.category,
            'sub_category': article.sub_category
            }
            return HttpResponseRedirect(self.request.path_info)

class AllArticlesView(DetailView):

        context_object_name = 'All'
        template_name = 'allarticles.html'
        model = Article

        def get(self, request, *args, **kwargs):

            all_articles = articles.models.Article.objects.all().order_by('-updated_at')
            context = {
                'articles' : all_articles,
                
            }

            return render(request, "allarticles.html", context=context)

