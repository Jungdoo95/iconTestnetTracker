from django.urls import path

from . import views

app_name='walletApp'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.createWallet, name='createWallet'),
    path('search/', views.searchWallet, name='searchWallet'),
]
