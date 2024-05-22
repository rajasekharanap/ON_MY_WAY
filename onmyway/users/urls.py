from . import views
from django.urls import path


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('logout/', views.user_logout, name="user_logout"),
    path('changepassword/', views.changepassword, name='changepassword')
]