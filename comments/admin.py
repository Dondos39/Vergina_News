from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'name', 'verified')

    list_filter = ('verified',)
    list_editable = ('verified',)

# Register your models here.
admin.site.register(Comment, CommentAdmin)
