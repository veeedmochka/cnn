from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Пользователь"""

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self) -> str:
        return self.username


class UserImage(models.Model):
    """Загружаемое фото"""
    title = models.CharField(max_length=10, unique=True, verbose_name='Название файла')
    image = models.ImageField(upload_to='images', verbose_name='Загружаемое фото')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Загружаемое фото'
        verbose_name_plural = 'Загружаемые фото'

    def __str__(self):
        return self.title