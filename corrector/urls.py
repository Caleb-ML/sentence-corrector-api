from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('correct/', views.correct_sentence, name='correct'),
]
