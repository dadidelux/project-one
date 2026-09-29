from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('', include(router.urls)),
]
