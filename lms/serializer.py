from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'lesson_count']

    def get_lesson_count(self, course):
        return Lesson.objects.filter(course_id=course.id).count()


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
