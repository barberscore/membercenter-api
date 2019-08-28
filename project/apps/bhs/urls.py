
# Third-Party
from rest_framework import routers

# Local
from .views import GroupViewSet
from .views import PersonViewSet

router = routers.DefaultRouter(
    trailing_slash=False,
)

router.register(r'group', GroupViewSet)
router.register(r'person', PersonViewSet)

urlpatterns = router.urls
