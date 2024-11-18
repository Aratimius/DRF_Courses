from typing import Dict, Any
from django.utils.timezone import now
from rest_framework.serializers import ModelSerializer
from users.models import User, Payment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'phone', 'city', 'avatar')


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class CustomTokenPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        """Запись в last_login текущей даты и времени"""
        data = super().validate(attrs)
        self.user.last_login = now()
        self.user.save()
        return data
