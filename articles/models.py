from django.db import models
import authors.models
import categories.models
import tags.models
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField
from django.conf import settings
from model_utils import FieldTracker
from VerginaNews.utils import get_img_path, get_video_path, image_size_validator
from django.utils.text import slugify

# Create your models here.
CATEGORIES = (("1", "Sports"),
               ("2", "People"),
               ("3", "Auto"),
               ("4", "Culture"),
               ("5", "Politics"),
               ("6", "Society"),
               ("7", "Business"),
               ("8", "Economy"),
)

IMPORTANT_N = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]

HOMEPAGE_N = [
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

class ArticleManager(models.Manager):
    def get_important(self):
        return self.filter(no_important__in=['1', '2', '3', '4', '5']).order_by('no_important')

    def get_latest(self):
        return self.order_by('-updated_at')[:10][::1]

    def get_frontnews(self):
        return self.filter(no_homepage__in=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])

    def get_popular(self):
        return self.order_by('-total_views')

    def get_featured(self):
        return self.filter(featured=True)

class Article(models.Model):
    ##  Attributes ##
    author = models.ManyToManyField(authors.models.Author)
    title = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=150, blank=True)
    date_added = models.DateField(("Date"), auto_now=True)
    time_added = models.TimeField(("Time"), auto_now=True)
    text = RichTextField()
    article_pic = models.ImageField(upload_to=get_img_path, blank=True, validators=[image_size_validator])
    article_video = models.FileField(upload_to=get_video_path,
                             null=True,
                             blank=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    url = models.URLField(max_length=256, blank=True)
    no_important = models.CharField(choices=IMPORTANT_N, max_length=6, null=True, blank=True)
    no_homepage =  models.CharField(choices=HOMEPAGE_N, max_length=9, null=True, blank=True)
    category = models.ForeignKey(categories.models.Category, on_delete=models.CASCADE, null=True)
    sub_category = models.ForeignKey(categories.models.SubCategory, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(tags.models.Tags, blank=True)
    featured = models.BooleanField(max_length=1, default=False)

    tracker = FieldTracker()
    objects = ArticleManager()

    ##  Logging  ##
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.CharField(max_length=32, blank=True, null=True)

    total_views = models.IntegerField(default=0)

    @property
    def article_id(self):
        return self.id

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_authors(self):
        return self.author.all().values_list('first_name', flat=True)

    def get_comments(self):
        return self.comment_set.all()

    def get_tags(self):
        return self.tags.all()

    def add_comment(self, dict):
        return self.comment_set.create(name=dict['author'], email=dict['email'], text=dict['text'])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.article_pic:
            self.article_pic.storage.delete(self.article_pic.name)

        if self.article_video:
            self.article_video.storage.delete(self.article_video.name)
        super().delete()
