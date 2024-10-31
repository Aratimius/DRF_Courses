from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from courses.models import Course, Lesson, Subscription
from courses.paginations import CustomPagination
from courses.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer, SubscriptionSerializer
from users.permissions import IsModer, IsOwner


#  Описываем ViewSet для Курсов:
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

    # def get_permissions(self):
    #     if self.action == 'create':
    #         self.permission_classes = (~IsModer,)
    #     elif self.action in ['list', 'update', 'retrieve']:
    #         self.permission_classes = (IsModer | IsOwner,)
    #     elif self.action == 'destroy':
    #         self.permission_classes = (IsOwner,)
    #     return super().get_permissions()


#  Описываем Generic-классы для Уроков:
class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.user = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination
    # permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated, IsModer | IsOwner]

    def perform_update(self, serializer):
        lesson = serializer.save()
        lesson.user = self.request.user
        lesson.save()


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionCreateAPIView(CreateAPIView):
    """Эндпоинт на создание и удаление подписки"""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        """Реализация создания и удаления подписки через метод post"""
        user = self.request.user
        # id курса, которое передал пользователь
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
