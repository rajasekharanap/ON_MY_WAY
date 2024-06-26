from . import views
from django.urls import path


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('otpverification/<str:phone>/', views.otp_verification, name='otpverification'),
    path('resetpassword/<str:phone>/', views.resetpassword, name='resetpassword'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('logout/', views.user_logout, name="user_logout"),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    path('deletecardetails/', views.delete_car_details, name='delete_car_details'),
    path('notifications', views.notifications, name='notifications'),
] 