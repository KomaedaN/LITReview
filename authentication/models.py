from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
from django.conf import settings


class User(AbstractUser):
    profil_pic = models.ImageField(verbose_name='photo de profil', blank=True)


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user',)
