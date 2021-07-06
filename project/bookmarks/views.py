from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from .models import Bookmarks, Folders
from .serializers import BookmarkSerializers, FoldersSerializers
from .pagination import Paginate


class FoldersView(viewsets.ModelViewSet):
    serializer_class = FoldersSerializers
    authentication_class = [BaseAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Folders.objects.filter(user=self.request.user)


class BookmarkView(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializers
    authentication_class = [BaseAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = Paginate

    def get_queryset(self):
        return Bookmarks.objects.filter(deleted_at__isnull=True, user=self.request.user)

    def list(self, request):
        try:
            queryset = self._filter_queryset_by_query(
                request, self.get_queryset())
            pages = self.paginate_queryset(queryset)

            serializer = BookmarkSerializers(pages, many=True)

            return self.get_paginated_response(serializer.data)

        except:
            return Response(data={}, status=HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        """
            delete bookmark item for ever
        """
        try:
            queryset = Bookmarks.objects.get(
                pk=kwargs['pk'], user=self.request.user)
            queryset.delete()
            return Response(data={"destroy": f"{queryset} was remove"}, status=HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['get'], detail=False, url_path="archive", url_name="archive")
    def archive(self, request):
        """
            List of all records sent to Archive from login user
        """
        queryset = Bookmarks.objects.filter(
            deleted_at__isnull=False, user=request.user)

        queryset = self._filter_queryset_by_query(request, queryset)

        pages = self.paginate_queryset(queryset)

        serializer = BookmarkSerializers(pages, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['get'], detail=True, url_path="archive", url_name="archive_item")
    def archive_item(self, request, pk=None):
        """
            detail for item (using pk) in archive from login user
        """
        try:
            queryset = Bookmarks.objects.get(
                deleted_at__isnull=False, user=request.user, pk=pk)
            serializer = BookmarkSerializers(queryset)
            return Response(data=serializer.data)
        except Bookmarks.DoesNotExist:
            return Response(data={'archive item': " Not found."}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['put'], detail=True, url_path="bookmark-trash", url_name="bookmark_trash")
    def bookmark_trash_item(self, request, pk=None):
        """
            send item to archive using pk from login user
        """
        try:
            queryset = Bookmarks.objects.get(
                deleted_at__isnull=True, user=request.user, pk=pk)
            queryset.deleted_at = timezone.now()
            queryset.save()
            return Response(data={'trashed': f" The {queryset} was sent to wastebasket"}, status=HTTP_202_ACCEPTED)
        except Bookmarks.DoesNotExist:
            return Response(data={'trashed': " Not found."}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['put'], detail=True, url_path="recover-item", url_name="recover_item")
    def bookmark_recover_item(self, request, pk=None):
        """
            recover item from wastebasket from login user
        """
        try:
            queryset = Bookmarks.objects.get(
                deleted_at__isnull=False, user=request.user, pk=pk)
            queryset.deleted_at = None
            queryset.save()
            return Response(data={'trashed': f" The {queryset} was recover"}, status=HTTP_202_ACCEPTED)
        except Bookmarks.DoesNotExist:
            return Response(data={'return item': " Not found."}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def _filter_queryset_by_query(self, request, queryset):
        """
            This function adds the filters to queryset from query in link
        """

        folder = request.GET.get('folder')
        if folder:
            queryset = queryset.filter(folder=folder)

        if request.GET.get('unsorted', False) in [True, "true", "1", 1, "yes"]:
            queryset = queryset.filter(folder__isnull=True)

        if request.GET.get('important', False) in [True, "true", "1", 1, "yes"]:
            queryset = queryset.filter(important=True)

        sort = request.GET.get('sort', 'default')
        if sort == "desc-date":
            queryset = queryset.order_by('created_at')
        elif sort == "title":
            queryset = queryset.order_by('title')
        elif sort == "desc-title":
            queryset = queryset.order_by('-title')

        return queryset
