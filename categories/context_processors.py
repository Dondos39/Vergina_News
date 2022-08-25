from  .models import Category
import ads.models

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)

def sidebar_ad(request):
    ad = ads.models.get_priority(10)
    return dict(ad=ad)
