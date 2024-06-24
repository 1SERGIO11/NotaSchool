from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Tariff(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tariffs')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.course.name}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField()

    def __str__(self):
        return f"Booking by {self.user.username} for {self.tariff.name}"
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Мужской'), ('female', 'Женский')), blank=True)

    def __str__(self):
        return self.user.username
class CoursePurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_purchases')
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, related_name='purchased_tariffs')
    purchase_date = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.tariff.course.name} - {self.tariff.name}"

# Создание или обновление данных профиля пользователя
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    profile, created = UserProfile.objects.get_or_create(user=instance)
    if not created:
        profile.save()
class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    video_url = models.FileField(upload_to='videos/')
    preview_url = models.ImageField(upload_to='images/')


    def __str__(self):
        return self.title
class LikedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_videos')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')
    liked_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.video.title}"
class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.video.title}'

class ViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='view_history')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='views')
    view_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} viewed {self.video.title} on {self.view_date.strftime('%Y-%m-%d %H:%M:%S')}"