from django.db import models
from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='название')
    image = models.ImageField(upload_to='courses/photo',blank=True, null=True, verbose_name='изображение')
    description = models.TextField(blank=True, null=True, verbose_name='описание')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=200, verbose_name='название')
    image = models.ImageField(upload_to='courses/photo',blank=True, null=True, verbose_name='изображение')
    description = models.TextField(blank=True, null=True, verbose_name='описание')
    link = models.CharField(max_length=200, blank=True, null=True, verbose_name='ссылка на видео')

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return self.title


class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
