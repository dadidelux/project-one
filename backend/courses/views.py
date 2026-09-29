from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
import uuid
from .models import Course, Chapter, Lesson, LessonProgress, Certificate
from .serializers import (
    CourseListSerializer,
    CourseDetailSerializer,
    ChapterSerializer,
    LessonSerializer,
    LessonProgressSerializer,
    CertificateSerializer,
)


class IsInstructorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_instructor


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsInstructorOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseListSerializer

    def get_queryset(self):
        queryset = Course.objects.all()
        if not self.request.user.is_authenticated or not self.request.user.is_instructor:
            queryset = queryset.filter(is_published=True)
        return queryset

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        course = self.get_object()
        course.is_published = True
        course.save()
        return Response({'status': 'published'})

    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        course = self.get_object()
        course.is_published = False
        course.save()
        return Response({'status': 'unpublished'})


class ChapterViewSet(viewsets.ModelViewSet):
    serializer_class = ChapterSerializer
    permission_classes = [IsInstructorOrReadOnly]

    def get_queryset(self):
        return Chapter.objects.filter(course_id=self.kwargs['course_pk'])

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs['course_pk'])


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsInstructorOrReadOnly]

    def get_queryset(self):
        return Lesson.objects.filter(chapter_id=self.kwargs['chapter_pk'])

    def perform_create(self, serializer):
        serializer.save(chapter_id=self.kwargs['chapter_pk'])


class LessonProgressViewSet(viewsets.ModelViewSet):
    serializer_class = LessonProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LessonProgress.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        progress = self.get_object()
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()
        return Response({'status': 'completed'})

    @action(detail=False, methods=['get'])
    def course_progress(self, request):
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response({'error': 'course_id required'}, status=status.HTTP_400_BAD_REQUEST)

        lessons = Lesson.objects.filter(chapter__course_id=course_id)
        completed = LessonProgress.objects.filter(
            user=request.user,
            lesson__in=lessons,
            completed=True
        ).count()

        return Response({
            'total_lessons': lessons.count(),
            'completed_lessons': completed,
            'progress_percentage': (completed / lessons.count() * 100) if lessons.count() > 0 else 0,
        })


class CertificateViewSet(viewsets.ModelViewSet):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_instructor:
            return Certificate.objects.all()
        return Certificate.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def issue(self, request):
        course_id = request.data.get('course_id')
        course = Course.objects.get(id=course_id)

        total_lessons = Lesson.objects.filter(chapter__course=course).count()
        completed_lessons = LessonProgress.objects.filter(
            user=request.user,
            lesson__chapter__course=course,
            completed=True
        ).count()

        if total_lessons == 0 or completed_lessons < total_lessons:
            return Response(
                {'error': 'Course not yet completed'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cert, created = Certificate.objects.get_or_create(
            user=request.user,
            course=course,
            defaults={'certificate_id': f'DSLMS-{uuid.uuid4().hex[:8].upper()}'}
        )

        if not created:
            return Response(CertificateSerializer(cert).data)

        return Response(CertificateSerializer(cert).data, status=status.HTTP_201_CREATED)
