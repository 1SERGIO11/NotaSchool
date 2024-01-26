from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    video_url = models.URLField()
    preview_url = models.URLField()


    def __str__(self):
        return self.title

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