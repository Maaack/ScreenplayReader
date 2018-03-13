from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'interpret-operations', views.InterpretOperationViewSet)
router.register(r'screenplays', views.ScreenplayViewSet)
router.register(r'lines', views.LineViewSet)
router.register(r'title-pages', views.TitlePageViewSet)
router.register(r'scenes', views.SceneViewSet)
router.register(r'locations', views.LocationViewSet)
router.register(r'characters', views.CharacterViewSet)

urlpatterns = router.urls
