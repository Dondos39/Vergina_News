from django.shortcuts import render
from django.views.generic.detail import DetailView
import articles

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
        articles = Article.objects.all().filter(category__name=category)
        context = {
                "category":articles.values_list('category__name', flat=True).first(),
                "articles": articles.order_by("-updated_at"),
        }
        return render(request, "category.html", context=context)

class SubCategoryView(DetailView):
    context_object_name = 'sub_category'
    template_name = 'sub_category.html'
    model = SubCategory

    def get(self, request, *args, **kwargs):
        sub_category = self.kwargs.get('sub_category')

        articles = Article.objects.all().filter(sub_category__slug = sub_category)
        context = {
                "category":articles.values_list('category__name', flat=True).first(),
                "sub_category":articles.values_list('sub_category__name', flat=True).first(),
                "articles": articles.order_by("-updated_at"),
        }
        return render(request, "sub_category.html", context=context)
