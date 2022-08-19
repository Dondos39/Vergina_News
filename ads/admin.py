from django.contrib import admin, messages
from .models import Ad, GoogleAd

def check_ad_priority(obj, request):
    duplicate = Ad.objects.filter(priority=obj.priority).values_list('id', flat=True)
    if duplicate.exists():
        for id in duplicate:
            Ad.objects.update_or_create(id=id, defaults={'priority': None})
            messages.warning(request, f"Ad {id} was changed to not show.")

def check_googlead_priority(obj, request):
    duplicate = GoogleAd.objects.filter(priority=obj.priority).values_list('id', flat=True)
    if duplicate.exists():
        for id in duplicate:
            GoogleAd.objects.update_or_create(id=id, defaults={'priority': None})
            messages.warning(request, f"Google Ad {id} was changed to not show.")

# Register your models here.
class AdAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_views', 'priority')
    readonly_fields = ['total_views']
    list_editable = ('priority',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.updated_by = str(request.user)
        prev_no_priority = obj.tracker.previous('priority')
        if obj.priority != prev_no_priority:
            check_ad_priority(obj, request)
            check_googlead_priority(obj, request)

        #Check if a new image is inserted when there is already one.
        if obj.id:
            old_ad_pic = Ad.objects.get(id=obj.id).ad_pic
        else:
            old_ad_pic = None
        if obj.ad_pic and old_ad_pic and old_ad_pic != obj.ad_pic:
            obj.ad_pic.storage.delete(str(old_ad_pic))
       #Check if user checked picture clear button.
        if request.POST.get('ad_pic-clear') == 'on':
            obj.ad_pic.storage.delete(str(old_ad_pic))

        super().save_model(request, obj, form, change)

class GoogleAdAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority')
    list_editable = ('priority',)

    def save_model(self, request, obj, form, change):
        prev_no_priority = obj.tracker.previous('priority')
        if obj.priority != prev_no_priority:
            check_ad_priority(obj, request)
            check_googlead_priority(obj, request)
        super().save_model(request, obj, form, change)

admin.site.register(Ad, AdAdmin)
admin.site.register(GoogleAd, GoogleAdAdmin)
