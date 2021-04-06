from django.db import models
from urllib.parse import urlparse


def get_path_site_icons(instance, filename):

    extend = filename.split('.')[1]
    baseurl = urlparse(instance.site_url).netloc
    image_path = f"sites/icons/{baseurl}.{extend}"
    return image_path


class Sites(models.Model):

    site_url = models.URLField(unique=True)
    icons = models.ImageField(
        upload_to=get_path_site_icons, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.site_url
