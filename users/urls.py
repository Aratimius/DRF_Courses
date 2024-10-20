from django.urls import path
from rest_framework.routers import SimpleRouter

from users.views import UserViewSet, PaymentListAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name

router = SimpleRouter()
router.register('', UserViewSet)

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name='payments_list'),

]
urlpatterns += router.urls
