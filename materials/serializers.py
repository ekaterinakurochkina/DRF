from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from users.serializer import PaymentsSerializer

class LessonSerializer(ModelSerializer):
    course = serializers.StringRelatedField()
    # course = CourseSerializer(read_only=True)
    payment = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ("id", "name", "description", "preview", "video_url", "course", "payment")

class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    payment = PaymentsSerializer(many=True, read_only=True)

    def get_lessons(self, course):
        return [lesson.name for lesson in course.lessons.all()]

    def get_lesson_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ("id", "name", "description", "preview", "lessons","lesson_count", "payment")


