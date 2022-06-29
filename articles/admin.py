from django.contrib import admin, messages
from .models import Article
from django import forms

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'time_added', 'no_important', 'no_homepage')
    list_editable = ('no_important', 'no_homepage')
    list_filter = ('no_important', 'date_added')
    search_fields = ['tags__name', 'author__first_name']
    readonly_fields = ['updated_at', 'updated_by']

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

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.updated_by = str(request.user)
        prev_no_homepage = obj.tracker.previous('no_homepage')
        prev_no_important = obj.tracker.previous('no_important')
        if obj.no_homepage != prev_no_homepage:
            self.check_no_homepage(obj, request)
        if obj.no_important != prev_no_important:
            self.check_no_important(obj, request)
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Article, ArticleAdmin)
