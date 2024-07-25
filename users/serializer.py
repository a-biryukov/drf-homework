from rest_framework.serializers import ModelSerializer

from users.models import Payments, User, Subscription


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'avatar', 'phone', 'country', 'password']


class PaymentsSerializer(ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'


class SubscriptionSerializer(ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
