from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Author

# Create your views here.
class AuthorView(DetailView):
        context_object_name = 'author'
        template_name = 'categories.html'
        model = Author

        def get(self, request, *args, **kwargs):
            id = self.kwargs.get('author_id')

            detail = Author.objects.all().filter(id=id)
            context = {
                    "detail": detail,
            }
            return render(request, "author.html", context=context)
