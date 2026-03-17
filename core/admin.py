from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, OTP, PsychometricTest, Question, AnswerOption,
    UserTestAttempt, UserAnswer, TestResult, UserProfile, CareerRecommendation
)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'is_verified', 'is_staff', 'created_at']
    list_filter = ['is_verified', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['email', 'username']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'is_verified')}),
    )

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'created_at', 'is_used']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email', 'code']
    ordering = ['-created_at']

@admin.register(PsychometricTest)
class PsychometricTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['test', 'question_text', 'question_type', 'order']
    list_filter = ['question_type', 'test__category']
    search_fields = ['question_text']
    ordering = ['test', 'order']

@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ['question', 'option_text', 'value', 'order']
    list_filter = ['question__test__category']
    search_fields = ['option_text', 'question__question_text']
    ordering = ['question', 'order']

@admin.register(UserTestAttempt)
class UserTestAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'status', 'total_score', 'started_at', 'completed_at']
    list_filter = ['status', 'test__category', 'started_at']
    search_fields = ['user__email', 'test__title']
    ordering = ['-started_at']

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'answered_at']
    list_filter = ['answered_at', 'question__question_type']
    search_fields = ['attempt__user__email', 'question__question_text']
    ordering = ['-answered_at']

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'generated_at']
    list_filter = ['generated_at']
    search_fields = ['attempt__user__email']
    ordering = ['-generated_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'education_level', 'current_field']
    list_filter = ['gender', 'education_level']
    search_fields = ['user__email', 'current_field']
    ordering = ['user']

@admin.register(CareerRecommendation)
class CareerRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'field', 'confidence_score', 'generated_at']
    list_filter = ['field', 'generated_at']
    search_fields = ['user__email', 'field']
    ordering = ['-confidence_score']
