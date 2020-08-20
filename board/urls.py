from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # ''는 아무것도 없는 것을 의미함 즉 localhost:8000 여기를 의미함
    path('', views.main_page, name='main_page'),
    # team 관련
    path('team_select/', views.team_select, name='team_select'),
    path('team_create/', views.team_create, name='team_create'),
    path('team_join/', views.team_join, name='team_join'),
    path('team_leave/<str:team_name_delete>', views.team_leave, name='team_leave'),
    path('team/<str:team_name>/', views.team_home, name='team_home'),
    # post 관련
    path('team/<str:team_name>/post_new/', views.post_new, name='post_new'),
]
