from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, CharField

from lms.models import Course, Lesson
from lms.validators import validate_urls
from users.models import Subscription


class LessonSerializer(ModelSerializer):
    name = CharField(validators=[validate_urls])
    description = CharField(validators=[validate_urls])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    name = CharField(validators=[validate_urls])
    description = CharField(validators=[validate_urls])
    lesson_count = SerializerMethodField()
    subscription = SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, course):
        return Lesson.objects.filter(course_id=course.id).count()

    def get_subscription(self, course):
        user = self.context.get('request').user
        return Subscription.objects.filter(course_id=course.id, user=user).exists()
