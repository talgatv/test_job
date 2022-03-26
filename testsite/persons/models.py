from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

def user_directory_path(instance, filename):
    return 'users/user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_directory_path )
    gender = models.CharField(max_length=25, choices=(("Male", "Мужской"),("Female", "Женский")) )


    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return 'User: {}'.format(self.user.username)


class Sympathies(models.Model):
    main = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='Cutie'
        )
    secondary = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='Romeo')

    class Meta:
        verbose_name = "Симпатия пользователя"
        verbose_name_plural = "Симпатии пользователей"

    def __str__(self):
        return f'{self.main} - {self.secondary}'
