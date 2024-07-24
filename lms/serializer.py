from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, CharField

from lms.models import Course, Lesson
from lms.validators import validate_urls


class LessonSerializer(ModelSerializer):
    name = CharField(validators=[validate_urls])
    description = CharField(validators=[validate_urls])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    name = CharField(validators=[validate_urls])
    description = CharField(validators=[validate_urls])

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, course):
        return Lesson.objects.filter(course_id=course.id).count()
