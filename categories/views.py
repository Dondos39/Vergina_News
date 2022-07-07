from django.shortcuts import render
from django.views.generic.detail import DetailView
import articles
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from articles.models import Article
from .models import Category , SubCategory
from django.views.generic.list import ListView


# Create your views here.
class CategoryView(DetailView):
    context_object_name = 'category'
    template_name = 'categories.html'
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category')
        detail = Article.objects.all().filter(category__name=category).order_by('-updated_at')
        paginator = Paginator(detail, 8)
        page = request.GET.get('page')
        page_articles = paginator.get_page(page)
        article_count = detail.count()
        context = {
                "detail": page_articles ,
                'article_count' : article_count, 
        }
        return render(request, "category.html", context=context)

class SubCategoryView(DetailView):
    context_object_name = 'sub_category'
    template_name = 'categories.html'
    model = SubCategory

    def get(self, request, *args, **kwargs):
        sub_category = self.kwargs.get('sub_category')
        print(sub_category)
        detail = Article.objects.all().filter(sub_category__slug = sub_category)
        context = {
                "detail": detail,
        }
        return render(request, "category.html", context=context)


