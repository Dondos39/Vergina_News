from django.db import models
import articles.models

# Create your models here.
class Comment(models.Model):
    article = models.ForeignKey(articles.models.Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    email = models.EmailField()
    text = models.CharField(max_length=512)
