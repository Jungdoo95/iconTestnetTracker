from django.urls import path

from . import views

app_name='geolocation'
urlpatterns = [
    path('', views.index, name='index'),
]
