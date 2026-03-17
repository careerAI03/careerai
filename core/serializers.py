from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    User, OTP, PsychometricTest, Question, AnswerOption,
    UserTestAttempt, UserAnswer, TestResult, UserProfile, CareerRecommendation
)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password', 'phone', 'name']
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        
        # Auto-generate username from name or email if not provided
        if not attrs.get('username'):
            if attrs.get('name'):
                # Generate username from name (lowercase, no spaces)
                base_username = attrs['name'].lower().replace(' ', '_')
            else:
                # Generate username from email
                base_username = attrs['email'].split('@')[0]
            
            username = base_username
            counter = 1
            
            # Ensure username is unique
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            attrs['username'] = username
        else:
            # Check if provided username already exists
            if User.objects.filter(username=attrs['username']).exists():
                raise serializers.ValidationError("Username already exists")
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data.pop('name', None)  # Remove name as it's not a User field
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user']

class PsychometricTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PsychometricTest
        fields = '__all__'

class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = '__all__'

class UserAnswerSerializer(serializers.ModelSerializer):
    selected_options = AnswerOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserAnswer
        fields = '__all__'

class UserTestAttemptSerializer(serializers.ModelSerializer):
    answers = UserAnswerSerializer(many=True, read_only=True)
    test = PsychometricTestSerializer(read_only=True)
    
    class Meta:
        model = UserTestAttempt
        fields = '__all__'

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'

class CareerRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerRecommendation
        fields = '__all__'
