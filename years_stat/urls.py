from django.urls import path, include
from . import views

app_name = 'years_stat'

urlpatterns = [
    path('', views.popularity, name = 'popularity'),
]