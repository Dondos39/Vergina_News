from django.contrib import admin
from .models import Author

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'job_title', 'email', 'featured')
    list_editable = ('featured',)

    def save_model(self, request, obj, form, change):
        old_prof_pic = Author.objects.get(id=obj.id).prof_pic
        if obj.prof_pic:
            if old_prof_pic:
                obj.prof_pic.storage.delete(str(old_prof_pic))

        if request.POST.get('prof_pic-clear') == 'on':
            obj.prof_pic.storage.delete(str(old_prof_pic))

        if obj.featured:
            temp = obj.__class__.objects.get(featured=True)
            if self != temp:
                temp.featured = False
                temp.save()
        super().save_model(request, obj, form, change)

admin.site.register(Author, AuthorAdmin)
