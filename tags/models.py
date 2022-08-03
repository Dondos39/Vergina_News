from django.db import models
import categories.models


class TagManager(models.Manager):
    def get_popular(self):
        return self.order_by('-total_views')

# Create your models here.
class Tags(models.Model):
    name = models.TextField()
    category = models.ManyToManyField(categories.models.Category, null=True)
    sub_category = models.ManyToManyField(categories.models.SubCategory, null=True)

    total_views = models.IntegerField(default=0)

    objects = TagManager()

    class Meta:
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name
    @classmethod
    def get_tags(self):
        return self.objects.values_list('id', 'name').distinct()
