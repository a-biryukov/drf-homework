from rest_framework.serializers import ModelSerializer

from users.models import Payments, User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'avatar', 'phone', 'country', 'password']


class PaymentsSerializer(ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'
