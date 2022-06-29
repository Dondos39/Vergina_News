from django.db import models
from django.utils.text import slugify

# Create your models here.
class CategoriesManager(models.Manager):
    def get_subcategories(self):
        return self.values_list('id', 'subcategory').distinct()

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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

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
