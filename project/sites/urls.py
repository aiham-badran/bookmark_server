from rest_framework.routers import DefaultRouter
from .views import SiteView

router = DefaultRouter()
router.register('', SiteView, basename="site")

urlpatterns = router.urls
