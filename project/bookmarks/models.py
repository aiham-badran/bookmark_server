from django.db import models
from django.contrib.auth.models import User
from sites.models import Sites


def get_path_file(instance, filename):
    image_path = f"bookmarks/{instance.user.username}/thumbnails/{filename}"
    return image_path


class Bookmarks(models.Model):

    url = models.URLField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    thumbnails = models.ImageField(
        upload_to=get_path_file, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    site = models.ForeignKey(Sites, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
