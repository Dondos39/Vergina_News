from django.contrib import admin, messages
from .models import Article
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class ArticleAdmin(admin.ModelAdmin):

    change_form_template = 'admin/article_change_form.html'

    def response_change(self, request, obj):
        if "_preview" in request.POST:
            url = reverse('article-preview', kwargs={'pk': obj.pk})
            return HttpResponseRedirect(url)
        return super().response_change(request, obj)

    list_display = ('title', 'date_added', 'time_added', 'no_important', 'no_homepage', 'featured')
    list_editable = ('no_important', 'no_homepage', 'featured')
    list_filter = ('no_important', 'category__name', 'date_added')
    search_fields = ['tags__name', 'author__first_name']
    readonly_fields = ['slug', 'updated_at', 'updated_by', 'total_views', 'date_added', 'time_added']

    fieldsets = (
        (None, {
            'fields': ('author', 'title', 'has_video', 'text', 'featured', 'article_pic', 'article_video', 'url', 'no_homepage', 'no_important', 'category', 'sub_category', 'tags')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('slug', 'updated_at', 'updated_by', 'total_views', 'date_added', 'time_added'),
        }),
        )

    def check_no_important(self, obj, request):
        duplicate = obj.__class__.objects.filter(no_important=obj.no_important).values_list('id', flat=True)
        if duplicate.exists():
            for id in duplicate:
                obj.__class__.objects.update_or_create(id=id, defaults={'no_important': None})
                messages.warning(request, f"Article {id} was changed to not show on important")

    def check_no_homepage(self, obj, request):
        duplicate = obj.__class__.objects.filter(no_homepage=obj.no_homepage).values_list('id', flat=True)
        if duplicate.exists():
            for id in duplicate:
                obj.__class__.objects.update_or_create(id=id, defaults={'no_homepage': None})
                messages.warning(request, f"Article {id} was changed to not show on homepage")

    def delete_model(self, request, obj):
            if obj.article_pic:
                obj.article_pic.storage.delete(str(obj.article_pic))
            if obj.article_video:
                obj.article_video.storage.delete(str(obj.article_video))
            super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for item in queryset.iterator():
            if item.article_pic:
                item.article_pic.storage.delete(str(item.article_pic))
            if item.article_video:
                item.article_video.storage.delete(str(item.article_video))
        super().delete_queryset(request, queryset)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.updated_by = str(request.user)
        prev_no_homepage = obj.tracker.previous('no_homepage')
        prev_no_important = obj.tracker.previous('no_important')
        if obj.no_homepage != prev_no_homepage:
            self.check_no_homepage(obj, request)
        if obj.no_important != prev_no_important:
            self.check_no_important(obj, request)

        if obj.id:
            old_article_pic = Article.objects.get(id=obj.id).article_pic
        else:
            old_article_pic = None
        if obj.article_pic and old_article_pic and old_article_pic != obj.article_pic:
            obj.article_pic.storage.delete(str(old_article_pic))

       #Check if user checked picture clear button.
        if request.POST.get('article_pic-clear') == 'on':
            if obj.no_homepage or obj.no_important:
                messages.warning(request, "Cannot delete image while the article is important/homepage")
                messages.set_level(request, messages.WARNING)
                obj.article_pic = old_article_pic
                return
            else:
                obj.article_pic.storage.delete(str(old_article_pic))
        else:
            if (obj.no_homepage or obj.no_important) and not obj.article_pic:
                messages.warning(request, "Important and Homepage articles are required to have an image")
                messages.set_level(request, messages.WARNING)
                return

       #Check if a new video is inserted when there is already one.
        if obj.id:
            old_article_video = Article.objects.get(id=obj.id).article_video
        else:
            old_article_video = None
        if obj.article_video and old_article_video and old_article_video != obj.article_video:
            obj.article_video.storage.delete(str(old_article_video))
       #Check if user checked video clear button.
        if request.POST.get('article_video-clear') == 'on':
            obj.article_video.storage.delete(str(old_article_video))

        # If featured is clicked check there not another one.
        if obj.featured:
            if Article.objects.get_featured().exists():
                temp = obj.__class__.objects.get(featured=True)
            else:
                temp = None
            if temp != None and self != temp:
                temp.featured = False
                temp.save()


        super().save_model(request, obj, form, change)

        

# Register your models here.
admin.site.register(Article, ArticleAdmin)
