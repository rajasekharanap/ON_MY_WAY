from . import views
from django.urls import path


urlpatterns = [
    path('', views.find, name='find'),
    path('book',views.book, name='book'),
]