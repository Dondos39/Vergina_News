from django.db import models
from django.utils.text import slugify
import articles.models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True, blank=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def id(self):
        return self.id

    def __str__(self):
        return self.name

    def get_subcategories(self):
        return self.subcategory_set.all()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_articles(self):
        return articles.models.Article.objects.all().filter(category__name=self.name).values('id', 'title', 'text', 'sub_category__name', 'date_added', 'time_added').order_by('updated_at')[:6][::-1]

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True, blank=True)
    class Meta:
        ordering = ('name', )
        verbose_name = 'sub-category'
        verbose_name_plural = 'Sub Categories'
    def subcategory_id(self):
        return self.id

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)
