from django.urls import path
from django.conf.urls import include
from importer import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'imported-content', views.ImportedContentViewSet)
router.register(r'parse-operations', views.ParseOperationViewSet)
router.register(r'interpret-operations', views.InterpretOperationViewSet)
router.register(r'text-block', views.TextBlockViewSet)
router.register(r'text-matches', views.TextMatchViewSet)
router.register(r'group-matches', views.GroupMatchViewSet)
router.register(r'screenplays', views.ScreenplayViewSet)
router.register(r'title-pages', views.TitlePageViewSet)
router.register(r'scenes', views.SceneViewSet)
router.register(r'locations', views.LocationViewSet)
router.register(r'characters', views.CharacterViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
