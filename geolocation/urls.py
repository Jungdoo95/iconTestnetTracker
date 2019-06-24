from django.urls import path

from . import views

app_name='geolocation'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.locationSearch, name='search'),
    path('insert/', views.insertArea, name='insertArea'),
    path('insert/editInfo/', views.editInfo, name='editInfo'),
]
