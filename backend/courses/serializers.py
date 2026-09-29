from rest_framework import serializers
from .models import Course, Chapter, Lesson, LessonProgress, Certificate


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'order', 'is_free']


class ChapterSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'description', 'order', 'lessons']


class CourseListSerializer(serializers.ModelSerializer):
    chapter_count = serializers.SerializerMethodField()
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'thumbnail', 'is_published', 'chapter_count', 'lesson_count', 'created_at']

    def get_chapter_count(self, obj):
        return obj.chapters.count()

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(chapter__course=obj).count()


class CourseDetailSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'thumbnail', 'is_published', 'chapters', 'created_at', 'updated_at']


class LessonProgressSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)

    class Meta:
        model = LessonProgress
        fields = ['id', 'lesson', 'lesson_title', 'completed', 'completed_at', 'last_accessed']
        read_only_fields = ['id', 'last_accessed']


class CertificateSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Certificate
        fields = ['id', 'user', 'username', 'course', 'course_title', 'issued_at', 'certificate_id']
        read_only_fields = ['id', 'issued_at', 'certificate_id']
