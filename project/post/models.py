from django.db import models
from django.contrib.auth.models import User

def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'
# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    writer=models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    like_count = models.PositiveIntegerField(default=0)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post=models.ForeignKey(Post, blank=False, null=False, on_delete=models.CASCADE, related_name='comments')
    writer=models.ForeignKey(User, on_delete=models.CASCADE)
    content=models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)