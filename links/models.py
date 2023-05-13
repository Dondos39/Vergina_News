from django.db import models

# Create your models here.
class Link(models.Model):
    
    name = models.TextField()
    url = models.URLField(max_length=256, blank=True)

    @property
    def link_id(self):
        return self.id

    def __str__(self):
        return self.name
