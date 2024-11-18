from datetime import datetime

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, CustomTokenPairSerializer
from users.services import create_price, create_stripe_session, create_product
from rest_framework_simplejwt.views import TokenObtainPairView


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Просмотр списка пользователей"
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Создание пользователя"
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="Просмотр пользователя"
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="Удаление пользователя"
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="Обновление пользователя"
))
class UserViewSet(ModelViewSet):
    """CRUD для пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # @action(detail=False, methods=('post',))
    # def last_login(self, request, pk):
    #     user = get_object_or_404(User, pk=pk)
    #     user.last_login = datetime.now()
    #     print(user.last_login)
    #     user.save()


class CustomTokenPairView(TokenObtainPairView):
    """Расширение класса TokenObtainPairView"""
    serializer_class = CustomTokenPairSerializer


class UserCreateAPIView(CreateAPIView):
    """регистрация пользователя через Generic-класс"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filterset_fields = ['course', 'lesson', 'payment_method']
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['payment_date']


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Создаем сессию для оплаты курса"""
        payment = serializer.save(user=self.request.user)
        course = payment.course
        amount = payment.payment_amount
        #  Создаем цену на основе стоимости и курса, которые указал пользователь
        #  Вообще нужно в модели курса и урока создать цену, потом ее просто передавать в create_price, по идее
        #  Но будем считать, что пользователь сам устанавливает цену за курс, хотя это тупо

        # продукт
        product = create_product(course)
        # цена
        price = create_price(amount, product)
        # сессия
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.product = product['name']
        payment.save()
