from django.db import models

# Create your models here.
class Link(models.Model):
    MEDIA_PLATFORM = (
        ('Facebook', 'Facebook' ),
        ('Instagram', 'Instagram' ),
        ('Twitch', 'Twitch' ),
        ('Twitter', 'Twitter' ),
        ('Linkedin', 'Linkedin' ),
        ('Youtube', 'Youtube' ),
        
    )
    
    name = models.TextField(choices=MEDIA_PLATFORM, unique=True)
    url = models.URLField(max_length=256, blank=True)

    @property
    def link_id(self):
        return self.id

    def __str__(self):
        return self.name
