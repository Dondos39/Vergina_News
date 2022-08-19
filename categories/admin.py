from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    readonly_fields = ['slug']

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')

    readonly_fields = ['slug']
    list_filter = ('category__name',)

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
