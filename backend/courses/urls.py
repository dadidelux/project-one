from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, ChapterViewSet, LessonViewSet, LessonProgressViewSet, CertificateViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'certificates', CertificateViewSet, basename='certificate')

urlpatterns = [
    path('', include(router.urls)),
    path('courses/<int:course_pk>/chapters/', ChapterViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('courses/<int:course_pk>/chapters/<int:pk>/', ChapterViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/lessons/', LessonViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('courses/<int:course_pk>/chapters/<int:chapter_pk>/lessons/<int:pk>/', LessonViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('progress/', LessonProgressViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('progress/<int:pk>/', LessonProgressViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('progress/<int:pk>/complete/', LessonProgressViewSet.as_view({'post': 'complete'})),
    path('progress/course-progress/', LessonProgressViewSet.as_view({'get': 'course_progress'})),
    path('certificates/issue/', CertificateViewSet.as_view({'post': 'issue'})),
]
