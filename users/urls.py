from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentsListAPIView, UserUpdateAPIView, UserCreateAPIView, UserRetrieveAPIView, \
    UserDestroyAPIView, UserListAPIView, SubscriptionAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user_register'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='user_login'),
    path('', UserListAPIView.as_view(), name='user_list'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user_delete'),
    path('payments/', PaymentsListAPIView.as_view(), name='user_payments'),
    path('subscription/', SubscriptionAPIView.as_view(), name='user_subscription')
]
