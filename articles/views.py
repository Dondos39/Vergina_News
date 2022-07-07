from django.shortcuts import render
from .models import Article
from categories.models import SubCategory
import articles.models
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
import json

# Create your views here.
def get_subcategory(request):
    id = request.GET.get('id', '')
    result = list(SubCategory.objects.filter(
    category_id=int(id)).values('id', 'name'))
    return HttpResponse(json.dumps(result), content_type="application/json")

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
            }
            return render(request, "article.html", context=context)

        def post(self, request, *args, **kwargs):
            id = request.POST.get('Article ID')
            print(id)
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
