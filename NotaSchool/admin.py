from django.contrib import admin
from .models import Video, Comment, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'birth_date', 'gender']
admin.site.register(Video)
admin.site.register(Comment)