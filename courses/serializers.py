from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from courses.models import Course, Lesson, Subscription
from courses.validators import LinkValidator


class CourseSerializer(ModelSerializer):
    sign_up = SerializerMethodField(read_only=True)

    def get_sign_up(self, instance):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=instance).exists()

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='link')]


class CourseDetailSerializer(ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True)

    class Meta:
        model = Course
        fields = '__all__'

    @staticmethod
    def get_lessons_count(instance):
        return instance.lesson_set.count()


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


# Мне так больше нравится, но задача требует другого решения(
    # @staticmethod
    # def get_lessons(instance):
    #     return [{'название': lesson.title, 'описание': lesson.description} for lesson in
    #             Lesson.objects.filter(courses=instance)]
