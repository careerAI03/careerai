from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
import random
import string
import requests
import json

from .models import (
    User, PsychometricTest, Question, AnswerOption,
    UserTestAttempt, UserAnswer, TestResult, UserProfile, CareerRecommendation
)
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, 
    PsychometricTestSerializer, QuestionSerializer, 
    UserTestAttemptSerializer, TestResultSerializer,
    UserProfileSerializer, CareerRecommendationSerializer
)

# Template Views
class HomeView(TemplateView):
    template_name = 'home.html'

class AuthView(TemplateView):
    template_name = 'auth.html'

class ProfileView(TemplateView):
    template_name = 'profile.html'

class TestView(TemplateView):
    template_name = 'test.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.request.GET.get('category', 'graduation')
        return context

class ResultsView(TemplateView):
    template_name = 'results.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attempt_id'] = self.request.GET.get('attempt_id')
        return context

def logout_view(request):
    logout(request)
    return redirect('home')

class CheckEmailView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        exists = User.objects.filter(email=email).exists()
        return Response({'exists': exists}, status=status.HTTP_200_OK)



class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Auto-verify user on registration
            user.is_verified = True
            user.save()
            
            # Automatically log in the user
            login(request, user)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Registration successful!',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'first_name': user.first_name
                }
            }, status=status.HTTP_201_CREATED)
        
        # Log the errors for debugging
        error_response = {}
        for field, errors in serializer.errors.items():
            if isinstance(errors, list):
                error_response[field] = errors[0] if errors else "Invalid value"
            else:
                error_response[field] = str(errors)
        
        return Response({
            'error': 'Registration failed',
            'details': error_response
        }, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request, username=email, password=password)
            
            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'message': 'Login successful',
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'username': user.username,
                        'first_name': user.first_name
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PsychometricTestListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tests = PsychometricTest.objects.all()
        serializer = PsychometricTestSerializer(tests, many=True)
        return Response(serializer.data)

class StartTestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            test_id = request.data.get('test_id')
            num_questions = request.data.get('num_questions', 15)  # Default to 15 questions
            
            print(f"Starting test with test_id: {test_id}, num_questions: {num_questions}")
            
            try:
                test = PsychometricTest.objects.get(id=test_id)
                print(f"Found existing test: {test}")
            except PsychometricTest.DoesNotExist:
                print(f"Test with id {test_id} not found, creating new one")
                # Create a default test if it doesn't exist
                category_map = {1: 'graduation'}
                category = category_map.get(int(test_id), 'graduation')
                
                test, created = PsychometricTest.objects.get_or_create(
                    category=category,
                    defaults={
                        'title': f'{category.title()} Test',
                        'description': f'Default {category} test'
                    }
                )
                
                print(f"Test creation result: created={created}, test={test}")
                
                if created:
                    # Create some default questions
                    self.create_default_questions(test)
                else:
                    # If test exists but has no questions, create them
                    if test.questions.count() == 0:
                        self.create_default_questions(test)
            
            # Check if user has an incomplete attempt
            existing_attempt = UserTestAttempt.objects.filter(
                user=request.user, 
                test=test, 
                status='in_progress'
            ).first()
            
            if existing_attempt:
                # Return existing questions for incomplete attempt
                existing_answers = existing_attempt.answers.all()
                answered_question_ids = [answer.question.id for answer in existing_answers]
                remaining_questions = test.questions.exclude(id__in=answered_question_ids)
                
                question_data = QuestionSerializer(remaining_questions, many=True).data
                
                return Response({
                    'attempt_id': existing_attempt.id,
                    'questions': question_data,
                    'message': 'You have an incomplete test. Continuing from where you left off.'
                }, status=status.HTTP_200_OK)
            
            # Create new attempt
            attempt = UserTestAttempt.objects.create(
                user=request.user,
                test=test
            )
            
            # Get 10 random questions from each field (60 total)
            selected_questions = []
            for field in ['technical', 'analytical', 'creative', 'business', 'social', 'medical']:
                field_questions = list(test.questions.filter(field=field))
                if len(field_questions) >= 10:
                    selected_field_questions = random.sample(field_questions, 10)
                else:
                    selected_field_questions = field_questions  # Take all if less than 10
                selected_questions.extend(selected_field_questions)
            
            # Shuffle all selected questions to mix them up
            random.shuffle(selected_questions)
            
            question_data = QuestionSerializer(selected_questions, many=True).data
            
            return Response({
                'attempt_id': attempt.id,
                'questions': question_data,
                'total_questions': len(question_data)
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"Error in StartTestView: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def create_default_questions(self, test):
        """Create default questions for a test"""
        questions_data = {
            'graduation': [
                ('I enjoy solving logical or mathematical problems', 'analytical'),
                ('I like working with computers and technology', 'technical'),
                ('I enjoy designing or creating new ideas', 'creative'),
                ('I like interacting and communicating with people', 'social'),
                ('I enjoy leading teams or making decisions', 'business'),
                ('I prefer structured problem-solving tasks', 'analytical'),
                ('I am curious about how software or apps work', 'technical'),
                ('I like visual creativity (design, UI, art)', 'creative'),
                ('I enjoy helping others and explaining things', 'social'),
                ('I am interested in business, startups or management', 'business'),
                ('I enjoy debugging and fixing problems', 'technical'),
                ('I like brainstorming new ideas', 'creative'),
                ('I am comfortable speaking in front of others', 'social'),
                ('I like planning and organizing tasks', 'business'),
                ('I enjoy working with data and numbers', 'analytical')
            ],
        }
        
        questions = questions_data.get(test.category, questions_data['graduation'])
        
        for i, (question_text, trait) in enumerate(questions[:15]):  # Create max 15 questions
            question = Question.objects.create(
                test=test,
                question_text=question_text,
                question_type='scale',  # Default to scale questions
                trait=trait,
                order=i + 1
            )
            
            # Create scale options (1-5)
            scale_options = [
                ('Strongly Disagree', 1),
                ('Disagree', 2),
                ('Neutral', 3),
                ('Agree', 4),
                ('Strongly Agree', 5)
            ]
            
            for j, (option_text, value) in enumerate(scale_options):
                AnswerOption.objects.create(
                    question=question,
                    option_text=option_text,
                    value=value,
                    order=j + 1
                )

class SubmitAnswerView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        attempt_id = request.data.get('attempt_id')
        question_id = request.data.get('question_id')
        selected_options = request.data.get('selected_options', [])
        scale_value = request.data.get('scale_value')
        
        try:
            attempt = UserTestAttempt.objects.get(
                id=attempt_id, 
                user=request.user, 
                status='in_progress'
            )
            question = Question.objects.get(id=question_id)
            
            # Create or update answer
            answer, created = UserAnswer.objects.update_or_create(
                attempt=attempt,
                question=question,
                defaults={
                    'scale_value': scale_value
                }
            )
            
            # Clear existing selected options and add new ones
            answer.selected_options.clear()
            if selected_options:
                answer.selected_options.add(*selected_options)
            
            return Response({
                'message': 'Answer saved successfully',
                'score': answer.calculate_score()
            }, status=status.HTTP_200_OK)
            
        except (UserTestAttempt.DoesNotExist, Question.DoesNotExist):
            return Response(
                {'error': 'Invalid attempt or question'},
                status=status.HTTP_404_NOT_FOUND
            )

class CompleteTestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        attempt_id = request.data.get('attempt_id')
        
        try:
            attempt = UserTestAttempt.objects.get(
                id=attempt_id, 
                user=request.user, 
                status='in_progress'
            )
            
            # Calculate total score
            total_score = sum(answer.calculate_score() for answer in attempt.answers.all())
            attempt.total_score = total_score
            attempt.status = 'completed'
            attempt.completed_at = timezone.now()
            attempt.save()
            
            # Generate test result and recommendations
            result = self.generate_test_result(attempt)
            
            return Response({
                'message': 'Test completed successfully',
                'total_score': total_score,
                'result': TestResultSerializer(result).data
            }, status=status.HTTP_200_OK)
            
        except UserTestAttempt.DoesNotExist:
            return Response(
                {'error': 'Invalid attempt'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def generate_test_result(self, attempt):
        # Calculate traits based on answers
        traits = self.calculate_traits(attempt)
        
        # Get deterministic degree recommendations
        recommended_degrees = self.map_to_degrees(traits)
        
        # Generate AI-powered recommendations using Gemini API
        result = TestResult.objects.create(attempt=attempt)
        
        # Store calculated traits
        result.personality_traits = traits
        
        # Generate AI recommendations
        ai_recommendations = self.get_gemini_recommendations(traits, recommended_degrees)
        
        # Store AI recommendations
        result.recommendations = ai_recommendations
        result.career_suggestions = recommended_degrees
        result.save()
        
        # Create career recommendations
        self.create_ai_career_recommendations(attempt.user, traits, recommended_degrees, attempt.test.category)
        
        return result
    
    def calculate_traits(self, attempt):
        """Calculate field scores from user answers"""
        traits = {
            "technical": 0,
            "analytical": 0,
            "creative": 0,
            "business": 0,
            "social": 0,
            "medical": 0
        }
        
        # Count questions per field for normalization
        field_counts = {
            "technical": 0,
            "analytical": 0,
            "creative": 0,
            "business": 0,
            "social": 0,
            "medical": 0
        }
        
        for answer in attempt.answers.all():
            field = answer.question.field
            
            # Skip if field is None or not in our field list
            if not field or field not in traits:
                continue
                
            # Calculate score based on question type
            if answer.question.question_type == 'yes_no':
                # Yes/No questions: Yes = +1, No = -1
                if answer.selected_options.exists():
                    selected_option = answer.selected_options.first()
                    traits[field] += selected_option.value
                    field_counts[field] += 1
            elif answer.question.question_type == 'single_choice':
                # Knowledge questions: Correct = +1, Incorrect = -1
                if answer.selected_options.exists():
                    selected_option = answer.selected_options.first()
                    traits[field] += selected_option.value
                    field_counts[field] += 1
        
        # Normalize to 0-1 scale based on maximum possible score per field (20 questions)
        for field in traits:
            max_possible_score = field_counts[field] * 1  # Max +1 per question
            if max_possible_score > 0:
                # Convert from range[-20, +20] to [0, 1]
                normalized_score = (traits[field] + max_possible_score) / (2 * max_possible_score)
                traits[field] = round(max(0, min(1, normalized_score)), 2)
            else:
                traits[field] = 0.0
        
        return traits
    
    def map_to_degrees(self, traits):
        """EXACT CAREER MAPPING LOGIC AS PROVIDED"""
        # Get sorted traits
        sorted_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)
        top_trait = sorted_traits[0][0]
        second_trait = sorted_traits[1][0]
        
        # Hybrid logic first (important)
        if top_trait == "technical" and second_trait == "analytical":
            return ["B.Tech Computer Science", "BCA", "B.Sc Data Science"]
        
        if top_trait == "business" and second_trait == "analytical":
            return ["BBA Finance", "B.Com", "Business Analytics"]
        
        if top_trait == "creative" and second_trait == "technical":
            return ["B.Des UX/UI", "Multimedia", "Animation"]
        
        if top_trait == "analytical" and second_trait == "social":
            return ["Psychology", "Behavioral Science"]
        
        if top_trait == "business" and second_trait == "social":
            return ["BBA Marketing", "HR Management", "Public Relations"]
        
        # Single trait fallback
        if top_trait == "technical":
            return ["BCA", "B.Tech Computer Science", "B.Sc IT"]
        
        elif top_trait == "analytical":
            return ["B.Sc Data Science", "B.Sc Mathematics", "B.Stat", "B.Tech AI/ML"]
        
        elif top_trait == "business":
            return ["BBA", "B.Com", "BMS", "BBM"]
        
        elif top_trait == "creative":
            return ["B.Des", "BA Media", "BA Fine Arts", "BFA"]
        
        elif top_trait == "social":
            return ["BA Psychology", "B.Ed", "BA Sociology", "Social Work"]
        
        elif top_trait == "medical":
            return ["B.Sc Biology", "B.Pharmacy", "B.Sc Nursing", "MBBS"]
        
        return ["BCA", "BBA"]
    
    def get_gemini_recommendations(self, traits, recommended_degrees):
        """Get AI-powered recommendations using Gemini API"""
        api_key = "AIzaSyBBCLVx9w_uxc1_aKUSRICdB0OPtzWlXt4"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        prompt = f"""
You are a career counselor.

User personality scores:
Analytical: {traits['analytical']}
Technical: {traits['technical']}
Creative: {traits['creative']}
Social: {traits['social']}
Business: {traits['business']}

Recommended degrees:
{recommended_degrees}

Task:
Explain WHY these bachelor degrees are suitable.

Rules:
- Output ONLY JSON
- No markdown
- No extra text

Format:
{{
  "ai_summary": "short clear explanation",
  "degree_explanations": [
    {{
      "degree": "BCA",
      "why_fit": "reason"
    }}
  ]
}}
"""
        
        try:
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }
            
            response = requests.post(url, json=payload, timeout=30)
            print("===== GEMINI RAW RESPONSE =====")
            print(response.text)
            
            if response.status_code == 200:
                response_data = response.json()
                content = response_data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                
                # CLEAN RESPONSE
                content = content.strip()

                # Remove markdown if present
                if content.startswith("```"):
                    content = content.split("```")[1]

                try:
                    return json.loads(content)
                except Exception as e:
                    print("RAW GEMINI OUTPUT:", content)
                    print("ERROR:", e)
                    return self.get_fallback_recommendations(traits, recommended_degrees)
            else:
                print(f"Gemini API error: {response.status_code} - {response.text}")
                return self.get_fallback_recommendations(traits, recommended_degrees)
                
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self.get_fallback_recommendations(traits, recommended_degrees)
    
    def get_fallback_recommendations(self, traits, recommended_degrees):
        """Fallback recommendations if Gemini API fails"""
        explanations = {}
        for degree in recommended_degrees:
            if degree in ["BCA", "B.Tech Computer Science"]:
                explanations[degree] = "Strong logical thinking and interest in software development"
            elif degree in ["BBA", "B.Com"]:
                explanations[degree] = "Good leadership and business orientation"
            elif degree in ["B.Des", "BA Media"]:
                explanations[degree] = "Creative thinking and design aptitude"
            elif degree in ["BA Psychology", "B.Ed"]:
                explanations[degree] = "Strong social skills and helping nature"
            else:
                explanations[degree] = "Well-rounded skills suitable for this field"
        
        return {
            "ai_summary": "Based on your responses, these degrees match your personality traits and strengths.",
            "degree_explanations": [
                {
                    "degree": degree,
                    "why_fit": explanations[degree]
                }
                for degree in recommended_degrees
            ]
        }
    
    def create_ai_career_recommendations(self, user, traits, recommended_degrees, category):
        """Create career recommendations based on traits and degrees"""
        # Determine field based on traits
        if traits.get("technical", 0) > 0.7:
            field = 'engineering'
        elif traits.get("analytical", 0) > 0.7:
            field = 'science'
        elif traits.get("creative", 0) > 0.7:
            field = 'design'
        elif traits.get("business", 0) > 0.7:
            field = 'management'
        elif traits.get("social", 0) > 0.7:
            field = 'education'
        else:
            field = 'commerce'
        
        # Calculate confidence score based on trait strength
        max_trait = max(traits.values())
        confidence = round(max_trait, 2)
        
        # Create career recommendation
        CareerRecommendation.objects.create(
            user=user,
            field=field,
            graduation_streams=recommended_degrees,
            confidence_score=confidence
        )

class UserTestHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        attempts = UserTestAttempt.objects.filter(user=request.user).order_by('-started_at')
        serializer = UserTestAttemptSerializer(attempts, many=True)
        return Response(serializer.data)

class CareerRecommendationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        recommendations = CareerRecommendation.objects.filter(user=request.user)
        serializer = CareerRecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)
