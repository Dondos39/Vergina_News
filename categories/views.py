from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
import articles
import ads.models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from articles.models import Article
from .models import Category , SubCategory
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect

# Create your views here.
class CategoryView(DetailView):
    context_object_name = 'category'
    template_name = 'categories.html'
    model = Category

    def get(self, request, *args, **kwargs):
        category_slug = self.kwargs.get('category')
        category = Category.objects.get(slug=category_slug)
        articles = Article.objects.filter(category__slug=category_slug).order_by('-updated_at')
        paginator = Paginator(articles, 8)
        page = request.GET.get('page')
        page_articles = paginator.get_page(page)
        article_count = articles.count()

        context = {
                "category": category.name,
                "description": category.description,
                "articles": page_articles ,
                'article_count' : article_count,
        }
        return render(request, "category.html", context=context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('ad_id'):
            id = request.POST.get('ad_id')
            ad = ads.models.Ad.objects.get(id=id)
            ad.total_views = ad.total_views + 1
            ad.save(update_fields=['total_views'])
            return HttpResponseRedirect(ad.url)

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

class SubCategoryView(DetailView):
    context_object_name = 'sub_category'
    template_name = 'sub_category.html'
    model = SubCategory

    def get(self, request, *args, **kwargs):
        subcategory_slug = self.kwargs.get('sub_category')
        subcategory = SubCategory.objects.get(slug=subcategory_slug)
        articles = Article.objects.filter(sub_category__slug = subcategory_slug).order_by('-updated_at')
        paginator = Paginator(articles, 8)
        page = request.GET.get('page')
        page_articles = paginator.get_page(page)
        article_count = articles.count()

        context = {
                "category": subcategory.category.name,
                "sub_category": subcategory.name,
                "description": subcategory.description,
                "articles": page_articles,
                "article_count": article_count,
        }
        return render(request, "sub_category.html", context=context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('ad_id'):
            id = request.POST.get('ad_id')
            ad = ads.models.Ad.objects.get(id=id)
            ad.total_views = ad.total_views + 1
            ad.save(update_fields=['total_views'])
            return HttpResponseRedirect(ad.url)

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
