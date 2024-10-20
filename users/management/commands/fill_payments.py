from django.core.management import BaseCommand

from courses.models import Course, Lesson
from users.models import User, Payment


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        """Команда для создания 2 платежей"""

        payment1 = {
            'user': User.objects.get(pk=1),
            'payment_date': '2022-01-01',
            'course': Course.objects.get(pk=2),
            'lesson': Lesson.objects.get(pk=1),
            'payment_amount': 100,
            'payment_method': 'наличные'
        }
        payment2 = {
            'user': User.objects.get(pk=1),
            'payment_date': '2022-10-01',
            'course': Course.objects.get(pk=2),
            'lesson': Lesson.objects.get(pk=2),
            'payment_amount': 50,
            'payment_method': 'перевод'
        }

        [Payment.objects.create(**payment) for payment in (payment1, payment2)]
        print('Payment created successfully.')
