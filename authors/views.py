from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
import ads.models
import articles
import categories.models
from .models import Author
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
class AuthorView(DetailView):
        #context_object_name = 'author'
        template_name = 'author.html'
        model = Author

        def get(self, request, *args, **kwargs):
            id = self.kwargs.get('author_id')

            author = Author.objects.filter(first_name=id).first()
            related_authors = Author.objects.filter(job_title=author.job_title).exclude(id=author.id)
            articles = author.get_articles().order_by('-updated_at')
            category = categories.models.Category.objects.filter(name=author.job_title).first()
            paginator = Paginator(articles, 12)
            page = request.GET.get('page')
            page_articles = paginator.get_page(page)
            article_count = articles.count()
            context = {
                    "author": author,
                    "articles": page_articles,
                    "article_count": article_count,
                    "related_authors": related_authors,
                    "tags": category.get_popular_tags(),
                    "ad_sidebar": ads.models.get_priority(9),
            }
            return render(request, 'author.html', context=context)

        def post(self, request, *args, **kwargs):
            keyword = request.POST.get('search')
            if keyword:
                if keyword == "":
                    result = 'all'
                else:
                    result = keyword
                return redirect('articles_view', search=result)
            else:
                request.session['email'] = request.POST.get('email_sub')
                return HttpResponseRedirect(request.path_info)
