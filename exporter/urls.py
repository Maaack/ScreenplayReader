from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'screenplays', views.ScreenplayViewSet)

urlpatterns = router.urls
