from django.urls import path
from rest_framework.routers import SimpleRouter

from courses.views import CourseViewSet, LessonListAPIView, LessonCreateAPIView, LessonDestroyAPIView, \
    LessonUpdateAPIView, LessonRetrieveAPIView, SubscriptionCreateAPIView, SubscriptionListAPIView
from courses.apps import CoursesConfig

app_name = CoursesConfig.name

router = SimpleRouter()
router.register('', CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name='lessons_list'),
    path("lessons/create/", LessonCreateAPIView.as_view(), name='lessons_create'),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name='lessons_delete'),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name='lessons_update'),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name='lessons_details'),
    path("subscription/create/", SubscriptionCreateAPIView.as_view(), name="subscription_create"),
    path("subscription/", SubscriptionListAPIView.as_view(), name="subscriptions"),
]
urlpatterns += router.urls
