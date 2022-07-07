from django.db import models

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

class Author(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    prof_pic = models.ImageField(upload_to='profile_pics', blank=True)
    email = models.EmailField()
    short_bio = models.CharField(max_length=512)
    job_title = models.CharField(max_length=10, choices=JOB_CHOICES)

    @property
    def author_id(self):
        return self.id

    def __str__(self):
        return self.first_name

    def get_job_title(self):
        print(self.job_title)
        return self.job_title
