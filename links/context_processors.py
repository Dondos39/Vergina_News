from .models import Link

def links(request):
    links = Link.objects.all()
    return dict(media_links=links)
