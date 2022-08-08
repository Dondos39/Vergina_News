from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView

import articles
from .models import Author
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
class AuthorView(DetailView):
        #context_object_name = 'author'
        template_name = 'author.html'
        model = Author

        def get(self, request, *args, **kwargs):
            id = self.kwargs.get('author_id')

            author = Author.objects.all().filter(first_name=id).first()
            articles = author.get_articles().order_by('-updated_at')
            paginator = Paginator(articles, 12)
            page = request.GET.get('page')
            page_articles = paginator.get_page(page)
            article_count = articles.count()           
            context = {
                    "author": author,
                    "articles": page_articles,
                    "article_count": article_count,
                    "other_authors": author.__class__.objects.filter(job_title=author.job_title).exclude(id=author.id)
            }
            return render(request, 'author.html', context=context)




