from django.contrib import admin
from .models import Tags


class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', )
    fields = ('category', 'sub_category', 'name', 'total_views')
    readonly_fields = ['total_views']

# Register your models here.
admin.site.register(Tags, TagsAdmin)
