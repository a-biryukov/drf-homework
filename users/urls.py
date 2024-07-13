from django.urls import path

from users.apps import UsersConfig
from users.views import PaymentsListAPIView, UserUpdateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('<int:pk>/update/', UserUpdateAPIView.as_view()),
    path('payments/', PaymentsListAPIView.as_view())
]
