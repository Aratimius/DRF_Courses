from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import UserViewSet, PaymentListAPIView, UserCreateAPIView, PaymentCreateAPIView, CustomTokenPairView
from users.apps import UsersConfig

app_name = UsersConfig.name

router = SimpleRouter()
router.register('', UserViewSet)

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name='payments_list'),
    path('login/', CustomTokenPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("register/", UserCreateAPIView.as_view(), name='register'),
    path("pay_course/", PaymentCreateAPIView.as_view(), name='pay_course'),

]
urlpatterns += router.urls
