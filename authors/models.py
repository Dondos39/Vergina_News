from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import articles.models
import uuid
import os
from model_utils import FieldTracker
from VerginaNews.utils import get_img_path, image_size_validator

# Create your models here.
JOB_CHOICES = (("1", "Sports"),
               ("2", "People"),
               ("3", "Auto"),
               ("4", "Culture"),
               ("5", "Politics"),
               ("6", "Society"),
               ("7", "Business"),
               ("8", "Economy"),
)

FEATURED_N = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
]

class AuthorManager(models.Manager):
        def get_featured(self):
            return self.filter(no_featured__in=['1', '2', '3']).order_by('no_featured')

class Author(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    prof_pic = models.ImageField(upload_to=get_img_path, blank=True, validators=[image_size_validator])
    email = models.EmailField()
    short_bio = models.CharField(max_length=512)
    job_title = models.CharField(max_length=10, choices=JOB_CHOICES)
    no_featured =  models.CharField(choices=FEATURED_N, max_length=4, null=True, blank=True)

    tracker = FieldTracker()
    objects= AuthorManager()

    @property
    def author_id(self):
        return self.id

    def __str__(self):
        return self.first_name

    def get_articles(self):
        return articles.models.Article.objects.filter(author__first_name=self.first_name)

    def get_job_title(self):
        return dict(JOB_CHOICES)[self.job_title]

    def delete(self, using=None, keep_parents=False):
        if self.prof_pic.url != None:
            self.prof_pic.storage.delete(self.prof_pic.name)
        super().delete()
