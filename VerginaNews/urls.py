"""VerginaNews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
import articles.views
import categories.views
import authors.views
from . import views

urlpatterns = [
    path(r's3cr3t4dm1n/', admin.site.urls),
    re_path(r'^getSubcategory/$', articles.views.get_subcategory),
    path('', views.HomepageViews.as_view(), name='home'),    
    path('search=<str:search>/', articles.views.AllArticlesView.as_view(), name='articles_view'),
    re_path('(?P<category>[\w\-]+)/$', categories.views.CategoryView.as_view(), name='category_view'),
    re_path('(?P<category>[\w\-]+)/(?P<sub_category>[\w\-]+)/$', categories.views.SubCategoryView.as_view(), name='subcategory_view'),
    re_path('(?P<category>[\w\-]+)/(?P<sub_category>[\w\-]+)/(?P<title>[\w-]+)/$', articles.views.ArticleView.as_view(), name='article_view'),
    re_path('^(?P<author_id>[\w\-]+)/$', authors.views.AuthorView.as_view(), name='author_view'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
