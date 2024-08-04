from datetime import timedelta

from django.utils import timezone
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from lms.paginators import CustomPaginator
from lms.permissions import IsModer, IsOwner
from lms.serializer import CourseSerializer, LessonSerializer
from users.tasks import sending_mails_to_subscribers
from users.models import Subscription


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPaginator

    def list(self, request, *args, **kwargs):

        if IsModer().has_permission(self.request, self):
            queryset = self.get_queryset().order_by('id')
        else:
            queryset = self.get_queryset().filter(owner=request.user).order_by('id')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated & ~IsModer]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            self.permission_classes = [IsModer | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def perform_update(self, serializer):
        course = serializer.save()
        now = timezone.now()
        if course:
            subscriptions = Subscription.objects.filter(course=course.id).exists()
            next_send_time = course.updated_at + timedelta(hours=4)

            if subscriptions and now > next_send_time:
                sending_mails_to_subscribers(course)

        course.updated_at = now
        course.save()


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & ~IsModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = CustomPaginator

    def get_queryset(self):
        if IsModer().has_permission(self.request, self):
            return Lesson.objects.all().order_by('id')
        else:
            return Lesson.objects.filter(owner=self.request.user).order_by('id')


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModer | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModer | IsOwner]

    def perform_update(self, serializer):
        course = serializer.save().course
        now = timezone.now()
        if course:
            subscriptions = Subscription.objects.filter(course=course.id).exists()
            next_send_time = course.updated_at + timedelta(hours=4)

            if subscriptions and now > next_send_time:
                sending_mails_to_subscribers(course)

        course.updated_at = now
        course.save()


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]
