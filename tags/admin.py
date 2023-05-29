from django.contrib import admin
from .models import Tags, TagCloud


class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', )
    fields = ('name','category', 'sub_category', 'total_views')
    readonly_fields = ['total_views']

class TagCloudAdmin(admin.ModelAdmin):
    filter_horizontal = ("tags",)


# Register your models here.
admin.site.register(Tags, TagsAdmin)
admin.site.register(TagCloud, TagCloudAdmin)
