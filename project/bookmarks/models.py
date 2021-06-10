from django.db import models
from django.contrib.auth.models import User
from sites.models import Sites


def get_path_file(instance, filename):
    image_path = f"bookmarks/{instance.user.username}/thumbnails/{filename}"
    return image_path


class Bookmarks(models.Model):

    url = models.URLField()
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    thumbnails = models.ImageField(
        upload_to=get_path_file, null=True, blank=True)
    important = models.BooleanField(null=True, blank=True, default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    site = models.ForeignKey(Sites, on_delete=models.CASCADE)
    folder = models.ForeignKey('Folders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Folders(models.Model):

    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=100, default='mdi-folder-outline')
    color = models.CharField(max_length=30, null=True,
                             blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey(
        to="self", null=True, blank=True, default=None, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
