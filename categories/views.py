from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Category , SubCategory
from .models import articles 
from django.views.generic.list import ListView

# Create your views here.
class CategoryView(DetailView):
    context_object_name = 'category'
    template_name = 'categories.html'
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category')

        detail = Category.objects.all().filter(name=category)
        context = {
                "detail": detail,
        }
        return render(request, "category.html", context=context)

class SubCategoryView(DetailView):
    context_object_name = 'sub_category'
    template_name = 'categories.html'
    model = SubCategory

    def get(self, request, *args, **kwargs):
        sub_category = self.kwargs.get('sub_category')

        detail = SubCategory.objects.all().filter(name=sub_category)
        context = {
                "detail": detail,
        }
        return render(request, "category.html", context=context)


