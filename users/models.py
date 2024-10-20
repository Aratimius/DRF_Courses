from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

from courses.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="почта")
    phone = models.CharField(
        max_length=35, blank=True, null=True, verbose_name="телефон"
    )
    city = models.CharField(max_length=150, blank=True, null=True, verbose_name="город")
    avatar = models.ImageField(
        upload_to="users/avatars", blank=True, null=True, verbose_name="аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='урок')

    payment_amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_date = models.DateField(default=date.today(), verbose_name='дата оплаты')
    payment_method = models.CharField(max_length=100, blank=True, null=True,
                                      verbose_name='способ оплаты: наличные или перевод на счет.')

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'

    def __str__(self):
        return self.payment_date
