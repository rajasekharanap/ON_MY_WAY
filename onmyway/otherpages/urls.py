from . import views
from django.urls import path


urlpatterns = [
    path('', views.working, name='working'),
    path('notifications', views.notifications, name='notifications'),
]