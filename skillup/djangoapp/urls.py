from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_user',views.create_user,name='create_user'),
    path('create_resource',views.create_resource,name='create_resource'),

    ]