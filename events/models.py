from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=120)
    image = models.FileField(null=True, blank=True)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    author = models.ForeignKey(User, default= '')


    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-timestamp", "-updated"]
