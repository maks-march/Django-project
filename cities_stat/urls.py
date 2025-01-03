from django.urls import path, include
from . import views

app_name = 'cities_stat'

urlpatterns = [
    path('', views.geography, name = 'geography'),
]