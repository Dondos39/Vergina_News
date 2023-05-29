from django.contrib import admin, messages
from .models import Author

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'no_featured', 'slug')
    list_editable = ('no_featured',)
    readonly_fields = ['slug']

    def check_no_featured(self, obj, request):
        duplicate = obj.__class__.objects.filter(no_featured=obj.no_featured).values_list('id', flat=True)
        if duplicate.exists():
            for id in duplicate:
                obj.__class__.objects.update_or_create(id=id, defaults={'no_featured': None})
                messages.warning(request, f"Author {id} was changed to not be featured")

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.updated_by = str(request.user)
        prev_no_featured = obj.tracker.previous('no_featured')
        if obj.no_featured != prev_no_featured:
            self.check_no_featured(obj, request)


        if obj.id:
            old_prof_pic = Author.objects.get(id=obj.id).prof_pic
        else:
            old_prof_pic = None
        if obj.prof_pic:
            if old_prof_pic:
                obj.prof_pic.storage.delete(str(old_prof_pic))

        if request.POST.get('prof_pic-clear') == 'on':
            obj.prof_pic.storage.delete(str(old_prof_pic))

        super().save_model(request, obj, form, change)

admin.site.register(Author, AuthorAdmin)
