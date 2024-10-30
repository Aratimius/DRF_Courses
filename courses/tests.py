from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="testoviy@gmail.com", password='0204')
        self.course = Course.objects.create(title="Java", user=self.user)
        self.lesson = Lesson.objects.create(title="Java", courses=self.course, user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('courses:lessons_update', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

