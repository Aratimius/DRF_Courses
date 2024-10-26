from rest_framework.serializers import ModelSerializer
from users.models import User, Payment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'phone', 'city', 'avatar')


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
