from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from .models import Bookmarks
from .serializers import BookmarkSerializers


class BookmarkView(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializers
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bookmarks.objects.filter(deleted_at__isnull=True, user=self.request.user)

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

    @action(methods=['get'], detail=False, url_path="wastebasket", url_name="wastebasket")
    def wastebasket(self, request):
        """
            List of all records sent to wastebasket from login user
        """
        queryset = Bookmarks.objects.filter(
            deleted_at__isnull=False, user=request.user)
        serializer = BookmarkSerializers(queryset, many=True)
        return Response(data=serializer.data)

    @action(methods=['get'], detail=True, url_path="wastebasket", url_name="wastebasket_item")
    def wastebasket_item(self, request, pk=None):
        """
            detail for item (using pk) in wastebasket from login user
        """
        try:
            queryset = Bookmarks.objects.get(
                deleted_at__isnull=False, user=request.user, pk=pk)
            serializer = BookmarkSerializers(queryset)
            return Response(data=serializer.data)
        except Bookmarks.DoesNotExist:
            return Response(data={'wastebasket item': " Not found."}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['put', 'get'], detail=True, url_path="bookmark-trash", url_name="bookmark_trash")
    def bookmark_trash_item(self, request, pk=None):
        """
            send item to wastebasket using pk from login user
        """
        try:
            queryset = Bookmarks.objects.get(
                deleted_at__isnull=True, user=request.user, pk=pk)
            print(queryset)
            queryset.deleted_at = timezone.now()
            queryset.save()
            return Response(data={'trashed': f" The {queryset} was sent to wastebasket"}, status=HTTP_202_ACCEPTED)
        except Bookmarks.DoesNotExist:
            return Response(data={'trashed': " Not found."}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['put', 'get'], detail=True, url_path="recover-item", url_name="recover_item")
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
