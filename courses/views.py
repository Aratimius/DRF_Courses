from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from courses.models import Course, Lesson, Subscription
from courses.paginations import CustomPagination
from courses.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer, SubscriptionSerializer
from courses.tasks import send_notification
from users.permissions import IsModer, IsOwner


#  Описываем ViewSet для Курсов:
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Просмотр списка курсов"
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Создание курса"
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="Просмотр курса"
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="Удаление курса"
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="Обновление курса"
))
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        """ Выбор сериализатора """
        if self.action == 'retrieve':  # если действие является детальным просмотром то:
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.user = self.request.user
        course.save()

    def perform_update(self, serializer):
        course = serializer.save()
        # отправить сообщение об обновлении курса подписанному пользователю:
        for subscription in Subscription.objects.filter(course=course.pk):
            email = subscription.user.email
            message = f'Данные по курсу "{subscription.course.title}" были обновлены'
            send_notification.delay(email, message)
        course.save()


#  Описываем Generic-классы для Уроков:
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Создание урока"
))
class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.user = self.request.user
        # отправить сообщение о создании урока подписанному пользователю:
        for subscription in Subscription.objects.filter(course=lesson.courses.pk):
            email = subscription.user.email
            message = f'В курсе "{subscription.course.title}" появился новый урок'
            send_notification.delay(email, message)
        lesson.save()


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Список уроков"
))
class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Просмотр одного урока"
))
class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


@method_decorator(name='patch', decorator=swagger_auto_schema(
    operation_description="Изменение урока"
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_description="Изменение урока"
))
class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]

    def perform_update(self, serializer):
        lesson = serializer.save()
        lesson.user = self.request.user
        # отправить сообщение об обновлении урока подписанному пользователю:
        for subscription in Subscription.objects.filter(course=lesson.courses.pk):
            email = subscription.user.email
            message = f'В курсе "{subscription.course.title}" обновился урок "{lesson.title}"'
            send_notification.delay(email, message)
        lesson.save()


@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_description="Удаление урока"
))
class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionCreateAPIView(CreateAPIView):
    """Эндпоинт на создание и удаление подписки"""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        """Реализация создания и удаления подписки через метод post"""
        user = self.request.user
        # id курса, который запросил пользователь
        course_id = self.request.data.get('course')
        # сущность курса, все данные по курсу, который запросил пользователь
        course_item = get_object_or_404(Course, pk=course_id)
        # queryset на сущность подписки фильтр по вошедшему пользователю и курсу
        subs_item = Subscription.objects.filter(course=course_item, user=user)

        if subs_item.exists(): #  если такая подписка существует то удаляем
            subs_item.delete()
            message = 'Подписка удалена'
        else:                  #  иначе создаем
            Subscription.objects.create(course=course_item, user=user)
            message = 'Подписка создана'

        return Response({'message': message})


class SubscriptionListAPIView(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
