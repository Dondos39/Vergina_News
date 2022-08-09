from django.db import models
import articles.models

# Create your models here.
class Comment(models.Model):
    article = models.ForeignKey(articles.models.Article, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=64)
    email = models.EmailField()
    text = models.CharField(max_length=512)
    verified = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.name
