from django.contrib import admin
from .models import Video, Comment, UserProfile
from .models import Course, Tariff, Booking, CoursePurchase, LikedVideo

admin.site.register(Course)
admin.site.register(Tariff)
admin.site.register(Booking)
admin.site.register(CoursePurchase)
admin.site.register(LikedVideo)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'birth_date', 'gender']
admin.site.register(Video)
admin.site.register(Comment)