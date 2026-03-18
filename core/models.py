from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random
import string

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email


class PsychometricTest(models.Model):
    CATEGORY_CHOICES = [
        ('graduation', 'Graduation Stream'),
    ]
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['category', 'title']
    
    def __str__(self):
        return f"{self.category} - {self.title}"

class Question(models.Model):
    QUESTION_TYPES = [
        ('single_choice', 'Single Choice'),
        ('multiple_choice', 'Multiple Choice'),
        ('scale', 'Scale 1-5'),
        ('yes_no', 'Yes/No'),
    ]
    
    FIELD_CHOICES = [
        ('technical', 'Technical'),
        ('analytical', 'Analytical'),
        ('creative', 'Creative'),
        ('business', 'Business'),
        ('social', 'Social'),
        ('medical', 'Medical'),
    ]
    
    test = models.ForeignKey(PsychometricTest, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    field = models.CharField(max_length=20, choices=FIELD_CHOICES, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.test.category} - Q{self.order}: {self.question_text[:50]}..."

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_options')
    option_text = models.CharField(max_length=200)
    value = models.IntegerField(default=0)  # Points for this answer
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.question.question_text[:30]}... - {self.option_text}"

class UserTestAttempt(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_attempts')
    test = models.ForeignKey(PsychometricTest, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    total_score = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'test', 'started_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.test.category} - {self.status}"

class UserAnswer(models.Model):
    attempt = models.ForeignKey(UserTestAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_options = models.ManyToManyField(AnswerOption, blank=True)
    scale_value = models.IntegerField(null=True, blank=True)  # For scale questions
    answer_text = models.TextField(blank=True)  # For text answers
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['attempt', 'question']
    
    def calculate_score(self):
        if self.question.question_type == 'scale':
            return self.scale_value or 0
        return sum(option.value for option in self.selected_options.all())
    
    def __str__(self):
        return f"{self.attempt.user.email} - {self.question.question_text[:30]}..."

class TestResult(models.Model):
    attempt = models.OneToOneField(UserTestAttempt, on_delete=models.CASCADE, related_name='result')
    recommendations = models.JSONField(default=dict)  # Store recommendations as JSON
    personality_traits = models.JSONField(default=dict)  # Store personality traits
    career_suggestions = models.JSONField(default=list)  # List of career suggestions
    generated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Result for {self.attempt.user.email} - {self.attempt.test.category}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)
    education_level = models.CharField(max_length=50, blank=True)
    current_field = models.CharField(max_length=100, blank=True)
    interests = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.email} Profile"

class CareerRecommendation(models.Model):
    FIELD_CHOICES = [
        ('science', 'Science & Technology'),
        ('commerce', 'Commerce & Finance'),
        ('arts', 'Arts & Humanities'),
        ('engineering', 'Engineering'),
        ('medicine', 'Medicine & Healthcare'),
        ('law', 'Law & Legal'),
        ('management', 'Management & Business'),
        ('design', 'Design & Creative'),
        ('education', 'Education & Research'),
        ('government', 'Government & Public Service'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='career_recommendations')
    field = models.CharField(max_length=50, choices=FIELD_CHOICES)
    graduation_streams = models.JSONField(default=list)
    confidence_score = models.FloatField(default=0.0)  # 0.0 to 1.0
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-confidence_score']
    
    def __str__(self):
        return f"{self.user.email} - {self.field} ({self.confidence_score:.2f})"
