from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("bookmarks/", include("bookmarks.urls")),
    path("sites/", include("sites.urls")),
]
