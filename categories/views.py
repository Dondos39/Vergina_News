from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Category

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
