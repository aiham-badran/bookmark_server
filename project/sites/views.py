from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED
from .models import Sites
from .serializers import SiteSerializers


class SiteView(viewsets.ModelViewSet):
    serializer_class = SiteSerializers
    queryset = Sites.objects.all()

    def destroy(self, request, *args, **kwargs):
        '''
            Ensure that the site is not linked with the bookmarks because in the event that 
            the site is deleted all the bookmarks linked to it will be permanently deleted
        '''
        children = Sites.objects.filter(pk=kwargs['pk']).first()
        if children.bookmarks_set.all().count() > 0:
            return Response({"Deleted_Error": f"There are several elements associated with {children}, so it cannot be deleted right now"}, status=HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
