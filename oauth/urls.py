from django.urls import path

from . import views

app_name='oauth'
urlpatterns = [
    path('', views.index, name='index'),
    path('input/email/', views.inputEmail, name='inputEmail'),
    path('input/profile/', views.inputProfile, name='inputProfile'),
    path('logout/', views.logout, name='logout'),
    path('kakao/login/', views.kakaoLogin, name='kakaologin'),
    path('kakao/response/', views.kakaoLoginResponse, name='kakaoResponse'),
    path('facebook/login/', views.facebookLogin, name='facebookLogin'),
    path('facebook/response/',views.facebookLoginResponse, name='facebookResponse'),
    path('google/login/', views.googleLogin, name='googleLogin'),
    path('google/response/', views.googleLoginResponse, name='googleLoginResponse'),
]
