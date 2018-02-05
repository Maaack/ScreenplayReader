from django.urls import path
from django.conf.urls import include
from importer import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'imported-content', views.ImportedContentViewSet)


urlpatterns = [
    path('', include(router.urls)),
]