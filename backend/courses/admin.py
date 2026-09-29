from django.contrib import admin
from .models import Course, Chapter, Lesson, LessonProgress, Quiz, Question, Choice, QuizAttempt


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'created_at']
    list_filter = ['is_published']
    search_fields = ['title', 'description']


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title']
    ordering = ['course', 'order']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'chapter', 'order', 'is_free']
    list_filter = ['chapter__course', 'is_free']
    search_fields = ['title', 'content']
    ordering = ['chapter', 'order']


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'completed', 'completed_at', 'last_accessed']
    list_filter = ['completed', 'lesson__chapter__course']
    search_fields = ['user__username', 'lesson__title']


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'passing_score']
    list_filter = ['lesson__chapter__course']
    search_fields = ['title']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'order']
    list_filter = ['quiz']
    inlines = [ChoiceInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'completed_at']
    list_filter = ['quiz', 'score']
    search_fields = ['user__username']
