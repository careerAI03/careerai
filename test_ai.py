#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careersai.settings')
django.setup()

from core.models import User, PsychometricTest, UserTestAttempt, Question, AnswerOption, UserAnswer, TestResult
from django.contrib.auth import get_user_model

def create_test_data():
    print("Creating test data...")
    
    # Get or create a test user
    User = get_user_model()
    user, created = User.objects.get_or_create(
        email='test@example.com',
        defaults={
            'username': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'is_verified': True
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print("Created test user")
    else:
        print("Using existing test user")
    
    # Create a psychometric test
    test, created = PsychometricTest.objects.get_or_create(
        category='graduation',
        defaults={
            'title': 'Career Guidance Test',
            'description': 'Test for career guidance'
        }
    )
    if created:
        print("Created psychometric test")
        
        # Create some questions
        questions_data = [
            "How interested are you in technology and programming?",
            "Do you enjoy solving complex mathematical problems?",
            "How comfortable are you with creative thinking and innovation?",
            "Do you prefer working in teams or independently?",
            "How important is leadership and management to you?"
        ]
        
        for i, question_text in enumerate(questions_data):
            question = Question.objects.create(
                test=test,
                question_text=question_text,
                question_type='scale',
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
        
        print("Created questions and options")
    
    # Create a test attempt
    attempt, created = UserTestAttempt.objects.get_or_create(
        user=user,
        test=test,
        defaults={'status': 'completed', 'total_score': 65}
    )
    
    if created:
        print("Created test attempt")
        
        # Create some answers
        questions = test.questions.all()
        for i, question in enumerate(questions):
            # Create realistic answers
            scale_value = 4 if i < 2 else 3  # First 2 questions strong agree, rest neutral
            answer = UserAnswer.objects.create(
                attempt=attempt,
                question=question,
                scale_value=scale_value
            )
        
        # Calculate total score
        total_score = sum(answer.calculate_score() for answer in attempt.answers.all())
        attempt.total_score = total_score
        attempt.status = 'completed'
        attempt.save()
        
        print(f"Created answers with total score: {total_score}")
    
    # Generate AI recommendations
    if not hasattr(attempt, 'result'):
        print("Generating AI recommendations...")
        from core.views import CompleteTestView
        view = CompleteTestView()
        result = view.generate_test_result(attempt)
        print("Generated AI recommendations")
        
        # Print the recommendations
        print("\n=== AI RECOMMENDATIONS ===")
        print(f"Personality Traits: {result.personality_traits}")
        print(f"Career Suggestions: {result.career_suggestions}")
        print(f"Recommendations: {result.recommendations}")
        
        if result.recommendations and 'recommended_degrees' in result.recommendations:
            print("\n=== RECOMMENDED DEGREES ===")
            for degree in result.recommendations['recommended_degrees']:
                print(f"- {degree.get('degree', 'Unknown')} (Confidence: {degree.get('confidence', 0):.2f})")
        
        if result.recommendations and 'ai_summary' in result.recommendations:
            print(f"\n=== AI SUMMARY ===")
            print(result.recommendations['ai_summary'])
    else:
        print("Result already exists")
        result = attempt.result
        print(f"Existing recommendations: {result.recommendations}")
    
    print(f"\nAttempt ID: {attempt.id}")
    print(f"User: {user.email}")
    print(f"Test Category: {test.category}")
    return attempt.id

if __name__ == '__main__':
    attempt_id = create_test_data()
    print(f"\nUse this URL to test: http://localhost:8000/results/?attempt_id={attempt_id}")
