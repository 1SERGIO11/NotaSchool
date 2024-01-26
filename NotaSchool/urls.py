from django.contrib import admin
from django.urls import path
from .views import check_username
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login_view'),
    path('login/', auth_views.LoginView.as_view(template_name='Вход.html'), name='login'),
    path('register/', views.register, name='register'),
    path('check_username/', check_username, name='check_username'),
    path('', views.home, name='home'),
    path('курсы/', views.courses_view, name='courses'),
    path('блог/', views.blog_view, name='blog'),
    path('разборы/', views.analysis_view, name='analysis'),
    path('user_home/', views.user_home, name='user_home'),
    path('profile/', views.profile, name='profile'),
    path('check_email/', views.check_email, name='check_email'),
    path('разборы/плеер/', views.player_view, name='player'),
]

