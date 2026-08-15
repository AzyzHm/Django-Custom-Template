from rest_framework.routers import DefaultRouter

from core.views.item_views import ItemViewSet

router = DefaultRouter()
router.register(r"items", ItemViewSet, basename="item")

urlpatterns = router.urls
