from django.urls import path, include
from . import views

app_name = 'skills_stat'

urlpatterns = [
    path('', views.skills, name = 'skills'),
]