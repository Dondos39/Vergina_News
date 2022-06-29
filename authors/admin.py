from django.contrib import admin
from .models import Author

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'job_title', 'email')

admin.site.register(Author, AuthorAdmin)
