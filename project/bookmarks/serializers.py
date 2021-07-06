from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from urllib.parse import urlparse
from .models import Bookmarks, Folders
from sites.models import Sites
from sites.serializers import SiteSerializers


class FoldersSerializers(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Folders
        exclude = ['user']

    def create(self, validated_data):
        '''
            send object from the current user a,
            When creating a new Folder
        '''
        user = self.context['request'].user  # get user login object
        folder = Folders.objects.create(
            **validated_data, user=user)
        return folder


class BookmarkSerializers(serializers.ModelSerializer):

    description = serializers.CharField(required=False)
    thumbnails = serializers.ImageField(allow_empty_file=True, required=False)
    site = SiteSerializers(read_only=True)
    folder = FoldersSerializers(read_only=True)
    folder_id = serializers.IntegerField(
        write_only=True, required=False)

    class Meta:
        model = Bookmarks
        exclude = ['user']
        read_only_fields = ['created_at', 'updated_at', 'deleted_at']

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

        # get folder objects
        # check if has folder id and has valid data get the folder
        if 'folder_id' in validated_data.keys() and validated_data['folder_id']:
            folder = Folders.objects.get(pk=validated_data['folder_id'])
        # if not has folder id  set folder none
        else:
            folder = None

        bookmark = Bookmarks.objects.create(
            **validated_data, user=user, site=site, folder=folder)
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
