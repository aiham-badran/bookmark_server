from rest_framework.routers import DefaultRouter
from .views import BookmarkView

router = DefaultRouter()
router.register('', BookmarkView, basename="bookmark")

urlpatterns = router.urls
