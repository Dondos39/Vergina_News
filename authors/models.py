from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import articles.models
import uuid
import os



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

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename_start = filename.replace('.'+ext,'')
    filename = "%s__%s.%s" % (uuid.uuid4(),filename_start, ext)
    return os.path.join('author_pics', filename)

class Author(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    prof_pic = models.ImageField(upload_to=get_file_path, blank=True)
    email = models.EmailField()
    short_bio = models.CharField(max_length=512)
    job_title = models.CharField(max_length=10, choices=JOB_CHOICES)
    featured = models.BooleanField(max_length=1, default=False)

    @property
    def author_id(self):
        return self.id

    def __str__(self):
        return self.first_name

    def get_articles(self):
        return articles.models.Article.objects.all().filter(author__first_name=self.first_name)

    def get_job_title(self):
        return dict(JOB_CHOICES)[self.job_title]

    def delete(self, using=None, keep_parents=False):
        if self.prof_pic.url != None:
            self.prof_pic.storage.delete(self.prof_pic.name)
        super().delete()
