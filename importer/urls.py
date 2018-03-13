from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'imported-content', views.ImportedContentViewSet)
router.register(r'parse-operations', views.ParseOperationViewSet)
router.register(r'text-block', views.TextBlockViewSet)
router.register(r'text-matches', views.TextMatchViewSet)
router.register(r'group-matches', views.GroupMatchViewSet)

urlpatterns = router.urls
