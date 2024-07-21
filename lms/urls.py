from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView

app_name = LmsConfig.name

router = SimpleRouter()
router.register('course', CourseViewSet)

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='detail'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='create'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='delete')
] + router.urls

