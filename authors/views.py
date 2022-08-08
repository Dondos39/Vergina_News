from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Author

# Create your views here.
class AuthorView(DetailView):
        #context_object_name = 'author'
        template_name = 'author.html'
        model = Author

        def get(self, request, *args, **kwargs):
            id = self.kwargs.get('author_id')

            author = Author.objects.filter(first_name=id).first()
            context = {
                    "author": author,
                    "articles": author.get_articles().order_by('-updated_at'),
                    "other_authors": author.__class__.objects.filter(job_title=author.job_title)

            }
            return render(request, 'author.html', context=context)

        def post(self, request, *args, **kwargs):
            keyword = request.POST.get('search')
            if keyword == "":
                result = 'all'
            else:
                result = keyword
            return redirect('articles_view', search=result)
