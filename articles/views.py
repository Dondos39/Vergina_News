from django.shortcuts import render
from django.shortcuts import render
from .models import Article
from categories.models import SubCategory
import articles.models
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from queue import Queue
import json

# Create your views here.
def get_subcategory(request):
    id = request.GET.get('id', '')
    result = list(SubCategory.objects.filter(
    category_id=int(id)).values('id', 'name'))
    return HttpResponse(json.dumps(result), content_type="application/json")

class ArticleView(DetailView):
        context_object_name = 'article'
        template_name = 'article.html'
        model = articles.models.Article
        def get(self, request, *args, **kwargs):
            post_id = self.kwargs.get('post_id')
            detail = articles.models.Article.objects.get(id=post_id)
            print(detail)
            context = {
            "detail": detail
            }
            print(context)
            return render(request, "article.html", context=context)
