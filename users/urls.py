from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentsListAPIView, UserUpdateAPIView, UserCreateAPIView, UserRetrieveAPIView, \
    UserDestroyAPIView, UserListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('', UserListAPIView.as_view(), name='list'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='detail'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='update'),
    path('<int:pk>/delete/', UserDestroyAPIView.as_view(), name='delete'),
    path('payments/', PaymentsListAPIView.as_view(), name='payments')
]
