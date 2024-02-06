from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter


from mes.users.views import UserViewSet
from mes.unit.views import UnitViewSet
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register('users',UserViewSet)
router.register('units',UnitViewSet)



app_name = "api"
urlpatterns = router.urls