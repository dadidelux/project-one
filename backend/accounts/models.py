from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_instructor = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username


class Enrollment(models.Model):
    ENROLLMENT_TYPE_CHOICES = [
        ('self', 'Self Enrolled'),
        ('admin', 'Admin Enrolled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='enrollments')
    enrollment_type = models.CharField(max_length=10, choices=ENROLLMENT_TYPE_CHOICES)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
