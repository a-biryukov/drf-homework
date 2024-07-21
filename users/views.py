
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from lms.permissions import IsModer, IsOwner
from users.models import Payments, User
from users.serializer import PaymentsSerializer, UserSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        print(user.password, user.email)
        user.set_password(user.password)
        print(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner]


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner]


class PaymentsListAPIView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('date_of_payment', )
