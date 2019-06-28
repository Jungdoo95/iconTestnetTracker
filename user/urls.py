from django.urls import path

# import views
from . import views

app_name='user'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('mypage/', views.mypage, name='mypage'),
    path('require/email/', views.inputEmail, name='inputEmail'),
    path('require/profile/', views.inputProfile, name='inputProfile'),
    path('logout/', views.logout, name='logout'),
    path('login/kakao/', views.kakaoLogin, name='kakaologin'),
    path('login/kakao/response/', views.kakaoLoginResponse, name='kakaoResponse'),
    path('login/facebook/', views.facebookLogin, name='facebookLogin'),
    path('login/facebook/response/',views.facebookLoginResponse, name='facebookResponse'),
    path('login/google/', views.googleLogin, name='googleLogin'),
    path('login/google/response/', views.googleLoginResponse, name='googleLoginResponse'),
]
