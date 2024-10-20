from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from courses.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseDetailSerializer(ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    # lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True)

    class Meta:
        model = Course
        fields = '__all__'

    @staticmethod
    def get_lessons_count(instance):
        return instance.lesson_set.count()




# Мне так больше нравится, но задача требует другого решения(
    # @staticmethod
    # def get_lessons(instance):
    #     return [{'название': lesson.title, 'описание': lesson.description} for lesson in
    #             Lesson.objects.filter(courses=instance)]
