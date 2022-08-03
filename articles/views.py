from django.shortcuts import render
from .models import Article
from categories.models import SubCategory
from subscribers.models import Subscriber
from tags.models import Tags
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.validators import validate_email
from django.contrib import messages
from django import forms
import json
# import requests
# Google captcha
from captcha.fields import ReCaptchaField

class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField()

# Create your views here.
def get_subcategory(request):
    id = request.GET.get('id', '')
    result = list(SubCategory.objects.filter(
    category_id=int(id)).values('id', 'name'))
    return HttpResponse(json.dumps(result), content_type="application/json")


class ArticleView(DetailView):
        context_object_name = 'articles'
        template_name = 'article.html'
        model = Article

        def get(self, request, *args, **kwargs):
            post_id = self.kwargs.get('post_id')

            detail = Article.objects.get(id=post_id)
            detail.total_views = detail.total_views + 1
            detail.save(update_fields=['total_views'])
            context = {
            "id": detail.id,
            "title": detail.title,
            "authors": detail.get_authors(),
            "updated_at":detail.updated_at,
            "comments": detail.get_comments(),
            "captcha": FormWithCaptcha,
            "category": detail.category.name,
            "sub_category": detail.sub_category.name,
            "related_articles": Article.objects.filter(category=detail.category, sub_category=detail.sub_category).exclude(id=detail.id),
            "total_views": detail.total_views,
            "tags": detail.get_tags(),
            "article_pic": detail.article_pic,
            "article_video": detail.article_video,
            }
            return render(request, "article.html", context=context)

        def post(self, request, *args, **kwargs):
            id = request.POST.get('Article ID')
            if id != None:
                article = Article.objects.get(id=id)
                comment = {
                   "author": request.POST.get('author'),
                   "email": request.POST.get('email'),
                   "text": request.POST.get('comment')
                }

                article.add_comment(comment)
                context = {
                   'post_id': article.id,
                   'category': article.category,
                   'sub_category': article.sub_category
                }

            email = request.POST.get('email_sub')
            if email != None:
                try:
                    validate_email(email)
                except forms.ValidationError:
                    messages.info(request, 'Please enter a correct email address.')
                if Subscriber.objects.filter(email=email).exists():
                        messages.info(request, 'Email Address already exists.')
                else:
                    sub = Subscriber(email=email)
                    sub.save()
            return HttpResponseRedirect(self.request.path_info)

class AllArticlesView(DetailView):
        context_object_name = 'All'
        template_name = 'allarticles.html'
        model = Article

        def get(self, request, *args, **kwargs):
            categories = Article.objects.all().values_list('category__name', flat=True).distinct()
            sub_categories = Article.objects.all().values_list('sub_category__name', flat=True).distinct()
            tags = Tags.objects.all().values_list('name', flat=True).distinct()
            if kwargs['search'] == 'all':
                articles = Article.objects.all().order_by('-updated_at')
            elif kwargs['search'] in tags:
                tag = Tags.objects.get(name=kwargs['search'])
                tag.total_views = tag.total_views + 1
                tag.save(update_fields=['total_views'])
                articles = Article.objects.filter(tags__name=kwargs['search']).order_by('-updated_at')
            else:
                articles = Article.objects.filter(title__icontains=kwargs['search']).order_by('-updated_at')
            context = {
                'articles' : articles,
            }
            return render(request, "allarticles.html", context=context)
