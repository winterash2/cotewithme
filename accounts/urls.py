from django.urls import path
from . import views
from board.views import main_page
from django.contrib.auth import views as auth_views


urlpatterns = [
    # localhost/accounts/login
    path('accounts/login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    # logout
    path('accounts/logout/', auth_views.LogoutView.as_view(), {'next_page': '/'}, name='logout'),
    # signup
    path('accounts/signup', views.signup, name='signup'),
]