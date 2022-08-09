from .models import Tags
import categories.models
import articles.models

def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

def tag_cloud(request, *args, **kwargs):
    path = request.get_full_path()
    values = path.split('/')
    values = [x.strip() for x in values if x.strip()]

    try:
        sub_category = values[1]
    except IndexError:
        sub_category = None
    try:
        category = values[0]
    except IndexError:
        category = None

    if  categories.models.SubCategory.objects.filter(slug=sub_category).exists():
        tags = categories.models.SubCategory.objects.filter(slug=sub_category).first().get_popular_tags()
        name = None
    elif categories.models.Category.objects.filter(slug=category).exists():
        tags = categories.models.Category.objects.filter(slug=category).first().get_popular_tags()
        name = None
    else:
        tags = None

    return dict(popular_tags=tags)
