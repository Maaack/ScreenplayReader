from django.urls import path
from . import views

urlpatterns = [
    path('', views.csv_preview, name='preview'),
    path('<int:screenplay_id>/', views.csv_export, name='detail'),
    path('<int:screenplay_id>/characters', views.csv_export_character_breakout, name='character'),
]