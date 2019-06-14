from django.urls import path

from . import views

app_name='walletApp'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.createWallet, name='createWallet'),
    path('create/close',views.walletCreateClose, name='createWalletClose'),
    path('create/keystore', views.keystoreDownload, name='downloadKeystore'),
    path('create/get/privateKey', views.walletPrivateKey, name='getPrivateKey'),
    path('search/', views.searchWallet, name='searchWallet'),
    path('search/upload/', views.uploadKeystore, name="uploadKeystore"),
]
