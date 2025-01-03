from django.urls import path, include
from . import views

app_name = 'last'

urlpatterns = [
    path('', views.last, name = 'last'),
]