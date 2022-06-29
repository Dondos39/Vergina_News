from django.db import models

# Create your models here.
class Tags(models.Model):
    name = models.TextField()

    class Meta:
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name
    @classmethod
    def get_tags(self):
        return self.objects.values_list('id', 'name').distinct()
