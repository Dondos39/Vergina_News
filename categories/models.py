from django.db import models
from django.utils.text import slugify
import articles.models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True, blank=True)
    description = models.CharField(max_length=150, null=True)

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

    def get_popular_tags(self):
        return self.tags_set.order_by('-total_views')

    def save(self, *args, **kwargs):
        greek_alphabet = 'ΑΆαάΒβΓγΔδΕΈεέΖζΗΉηήΘθΙΊιίϊΐΚκΛλΜμΝνΞξΟΌοόΠπΡρΣσςΤτΥΎυύΦφΧχΨψΩΏωώ'
        latin_alphabet = 'AAaaBbGgDdEEeeZzHHhh88IIiiiiKkLlMmNnXxOOooPpRrSssTtYYyyFfXxCcWWww'
        greek2latin = str.maketrans(greek_alphabet, latin_alphabet)

        latin = self.name.translate(greek2latin)
        self.slug = slugify(latin)
        super(Category, self).save(*args, **kwargs)

    def get_articles(self):
        return articles.models.Article.objects.all().filter(category__name=self.name).filter(publish=True).order_by('-updated_at')[:6][::1]

    def get_featured(self):
        return articles.models.Article.objects.filter(featured=True)


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True, blank=True)
    description = models.CharField(max_length=150, null=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'sub-category'
        verbose_name_plural = 'Sub Categories'
    def subcategory_id(self):
        return self.id

    def __str__(self):
        return self.name

    def get_popular_tags(self):
        return self.tags_set.order_by('-total_views')

    def save(self, *args, **kwargs):
        greek_alphabet = 'ΑαΒβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσςΤτΥυΦφΧχΨψΩω'
        latin_alphabet = 'AaBbGgDdEeZzHhJjIiKkLlMmNnXxOoPpRrSssTtUuFfQqYyWw'
        greek2latin = str.maketrans(greek_alphabet, latin_alphabet)

        latin = self.name.translate(greek2latin)
        self.slug = slugify(latin)
        super(SubCategory, self).save(*args, **kwargs)
