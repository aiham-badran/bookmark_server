from rest_framework.routers import DefaultRouter
from .views import BookmarkView, FoldersView

router = DefaultRouter()
router.register('folders', FoldersView, basename="folder")
router.register('', BookmarkView, basename="bookmark")


urlpatterns = router.urls
