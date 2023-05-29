from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import articles.models
import uuid
import os
from model_utils import FieldTracker
from VerginaNews.utils import get_img_path, image_size_validator
from django_resized import ResizedImageField
from django.utils.text import slugify
import categories.models

# Create your models here.
FEATURED_N = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
]

class AuthorManager(models.Manager):
        def get_featured(self):
            return self.filter(no_featured__in=['1', '2', '3']).order_by('no_featured')

class Author(models.Model):
    name = models.CharField(max_length=64, blank=True)
    prof_pic = ResizedImageField(upload_to=get_img_path, blank=True, validators=[image_size_validator])
    slug = models.SlugField(max_length=150, unique=True, db_index=True, blank=True)
    email = models.EmailField()
    short_bio = models.CharField(max_length=512)
    no_featured =  models.CharField(choices=FEATURED_N, max_length=4, null=True, blank=True)

    tracker = FieldTracker()
    objects= AuthorManager()

    @property
    def author_id(self):
        return self.id

    def __str__(self):
        return self.name

    def get_articles(self):
        return articles.models.Article.objects.filter(author__name=self.name).filter(publish=True)

    def save(self, *args, **kwargs):
        greek_alphabet = 'ΑΆαάΒβΓγΔδΕΈεέΖζΗΉηήΘθΙΊιίϊΐΚκΛλΜμΝνΞξΟΌοόΠπΡρΣσςΤτΥΎυύΦφΧχΨψΩΏωώ'
        latin_alphabet = 'AAaaBbGgDdEEeeZzHHhh88IIiiiiKkLlMmNnXxOOooPpRrSssTtYYyyFfXxCcWWww'
        greek2latin = str.maketrans(greek_alphabet, latin_alphabet)

        latin = self.name.translate(greek2latin)
        self.slug = slugify(latin)
        super(Author, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.prof_pic.url != None:
            self.prof_pic.storage.delete(self.prof_pic.name)
        super().delete()
