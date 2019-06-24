from django.urls import path

from . import views

app_name='geolocation'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.locationSearch, name='search'),
    path('insert/', views.insertArea, name='insertArea'),
<<<<<<< HEAD
    path('insert/editInfo/', views.editInfo, name='editInfo'),
=======
>>>>>>> b9adcce0e6e1a246ccd7455f54d68b0a8efb7ee8
]
