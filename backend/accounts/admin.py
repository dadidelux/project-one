from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Enrollment


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_instructor', 'is_staff']
    list_filter = ['is_instructor', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('is_instructor', 'phone', 'avatar')}),
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'enrollment_type', 'enrolled_at', 'is_active']
    list_filter = ['enrollment_type', 'is_active', 'course']
    search_fields = ['user__username', 'course__title']
