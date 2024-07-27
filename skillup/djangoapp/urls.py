from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_user',views.create_user,name='create_user'),
    path('create_resource',views.create_resource,name='create_resource'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('search-results',views.search,name='search-results'),
    path('profile',views.profile,name='profile'),
    path('resource/<str:id>',views.get_resource,name='resource'),
    ]