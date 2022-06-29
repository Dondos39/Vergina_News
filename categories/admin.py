from django.contrib import admin
from .models import *

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')

# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory, SubCategoryAdmin)
