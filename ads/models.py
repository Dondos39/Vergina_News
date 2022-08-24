from django.db import models
from model_utils import FieldTracker
import os
import uuid
from VerginaNews.utils import get_img_path

PRIORITY_N = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
]

def get_priority(num):
    if num < 11 and num > 0:
        ad = Ad.objects.get_priority(num)
        if ad.exists():
            return ad

        ad = GoogleAd.objects.get_priority(num)
        if ad.exists():
            return ad
    return None

class ArticleManager(models.Manager):
    def get_priority(self, num):
        if num < 11 and num > 0:
            return self.filter(priority__in=[str(num)])
        return 0

# Create your models here.
class Ad(models.Model):
    name =  models.CharField(max_length=64, unique=True, db_index=True)
    ad_pic = models.ImageField(upload_to=get_img_path, blank=True)
    url = models.URLField(max_length=256)
    priority = models.CharField(choices=PRIORITY_N, max_length=10, null=True, blank=True)

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

class GoogleAd(models.Model):
    name =  models.CharField(max_length=64, unique=True, db_index=True)
    widget = models.CharField(max_length=4096, null=True)
    priority = models.CharField(choices=PRIORITY_N, max_length=10, null=True, blank=True)

    tracker = FieldTracker()
    objects = ArticleManager()

    @property
    def article_id(self):
        return self.id

    def __str__(self):
        return self.name
