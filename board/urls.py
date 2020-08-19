from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # ''는 아무것도 없는 것을 의미함 즉 localhost:8000 여기를 의미함
    path('', views.main_page, name='main_page'),
    path('team_select/', views.team_select, name='team_select'),
    path('team_create/', views.team_create, name='team_create'),
    path('team_join/', views.team_join, name='team_join'),
]