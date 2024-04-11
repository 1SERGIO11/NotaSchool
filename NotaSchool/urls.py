from django.contrib import admin
from .views import check_username, course_view
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login_view'),
    path('login/', auth_views.LoginView.as_view(template_name='Вход.html'), name='login'),
    path('register/', views.register, name='register'),
    path('check_username/', check_username, name='check_username'),
    path('', views.home, name='home'),
    path('курсы/', views.courses_view, name='courses'),
    path('блог/', views.blog_view, name='blog'),
    path('разборы/', views.analysis_page, name='analysis'),
    path('user_home/', views.user_home, name='user_home'),
    path('profile/', views.profile, name='profile'),
    path('check_email/', views.check_email, name='check_email'),
    path('разборы/плеер/<int:video_id>/', views.player_view, name='player'),
    path('add_comment/<int:video_id>/', views.add_comment, name='add_comment'),
    path('logout/', logout_view, name='logout'),
    path('курсы/курс-1/', course_view, name='course-1')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

