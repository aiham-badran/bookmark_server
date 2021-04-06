from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from urllib.parse import urlparse
from .models import Bookmarks
from sites.models import Sites
from sites.serializers import SiteSerializers


class BookmarkSerializers(serializers.ModelSerializer):

    description = serializers.CharField(required=False)
    thumbnails = serializers.ImageField(allow_empty_file=True, required=False)
    site = SiteSerializers(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    deleted_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Bookmarks
        exclude = ['user']

    def create(self, validated_data):
        '''
            send object from the current user and object form site using url,
            When creating a new bookmark
        '''
        user = self.context['request'].user  # get user login object
        url_parse = urlparse(validated_data['url'])  # parse url
        # set scheme and url name only
        base_url = f"{url_parse.scheme}://{url_parse.netloc}"
        site = self._get_site_objects_or_create(
            base_url)  # get object from site table

        bookmark = Bookmarks.objects.create(
            **validated_data, user=user, site=site)
        return bookmark

    def _get_site_objects_or_create(self, url):
        """
            Searches the database for the url, if finds it, the function  
            return this object else create it, and return created object
        """
        site = Sites.objects.filter(site_url=url).first()
        if not site:  # if site is None
            site = Sites.objects.create(site_url=url)
            site.save()
        return site
