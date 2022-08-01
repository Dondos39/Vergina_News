from django.db import models
from model_utils import FieldTracker
import os
import uuid

PRIORITY_N = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename_start = filename.replace('.'+ext,'')
    filename = "%s__%s.%s" % (uuid.uuid4(),filename_start, ext)
    return os.path.join('ads_pics', filename)

class ArticleManager(models.Manager):
    def get_priority(self, num):
        if num < 6 and num > 0:
            return self.filter(priority__in=[str(num)])
        return 0

# Create your models here.
class Ad(models.Model):
    name =  models.CharField(max_length=64, unique=True)
    ad_pic = models.ImageField(upload_to=get_file_path, blank=True)
    url = models.URLField(max_length=256)
    priority = models.CharField(choices=PRIORITY_N, max_length=6, null=True, blank=True)

    total_views = models.IntegerField(default=0)

    tracker = FieldTracker()
    objects = ArticleManager()

    @property
    def article_id(self):
        return self.id

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        if self.ad_pic:
            self.ad_pic.storage.delete(self.ad_pic.name)
        super().delete()
