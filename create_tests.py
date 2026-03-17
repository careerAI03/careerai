#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careersai.settings')
django.setup()

from core.models import PsychometricTest, Question, AnswerOption

def create_sample_tests():
    # Create Graduation Test
    grad_test, created = PsychometricTest.objects.get_or_create(
        category='graduation',
        title='Undergraduate Stream Selection Test',
        defaults={
            'description': 'Helps students choose the right undergraduate program based on their personality and interests'
        }
    )

    if created:
        # Sample questions for graduation test
        graduation_questions = [
            {
                'text': 'How comfortable are you with mathematics and logical problem-solving?',
                'type': 'scale',
                'options': []
            },
            {
                'text': 'Which type of work environment do you prefer?',
                'type': 'single_choice',
                'options': [
                    ('Office/Collaborative setting', 1),
                    ('Laboratory/Research environment', 2),
                    ('Remote/Flexible work', 3),
                    ('Field work/Outdoor', 4)
                ]
            },
            {
                'text': 'Do you enjoy working with computers and technology?',
                'type': 'yes_no',
                'options': []
            },
            {
                'text': 'What interests you most?',
                'type': 'multiple_choice',
                'options': [
                    ('Solving complex problems', 3),
                    ('Creative expression', 2),
                    ('Helping others', 3),
                    ('Business and finance', 2)
                ]
            },
            {
                'text': 'How do you prefer to learn new things?',
                'type': 'single_choice',
                'options': [
                    ('Through hands-on practice', 3),
                    ('By reading and studying theory', 2),
                    ('Through group discussions', 2),
                    ('By watching demonstrations', 1)
                ]
            }
        ]

        for i, q_data in enumerate(graduation_questions):
            question = Question.objects.create(
                test=grad_test,
                question_text=q_data['text'],
                question_type=q_data['type'],
                order=i + 1
            )
            
            # Create answer options if provided
            for option_text, value in q_data['options']:
                AnswerOption.objects.create(
                    question=question,
                    option_text=option_text,
                    value=value,
                    order=len(question.answer_options.all()) + 1
                )

        print(f'Created graduation test with ID: {grad_test.id}')
    else:
        print(f'Graduation test already exists with ID: {grad_test.id}')

    # Create Post Graduation Test
    postgrad_test, created = PsychometricTest.objects.get_or_create(
        category='post_graduation',
        title='Postgraduate Program Selection Test',
        defaults={
            'description': 'Helps graduates choose the right postgraduate program based on their career goals'
        }
    )

    if created:
        # Sample questions for post graduation test
        postgrad_questions = [
            {
                'text': 'What is your primary career goal?',
                'type': 'single_choice',
                'options': [
                    ('Academic research and teaching', 3),
                    ('Industry leadership role', 3),
                    ('Specialized technical expertise', 2),
                    ('Entrepreneurship', 2)
                ]
            },
            {
                'text': 'How interested are you in research and academic writing?',
                'type': 'scale',
                'options': []
            }
        ]

        for i, q_data in enumerate(postgrad_questions):
            question = Question.objects.create(
                test=postgrad_test,
                question_text=q_data['text'],
                question_type=q_data['type'],
                order=i + 1
            )
            
            for option_text, value in q_data['options']:
                AnswerOption.objects.create(
                    question=question,
                    option_text=option_text,
                    value=value,
                    order=len(question.answer_options.all()) + 1
                )

        print(f'Created postgraduation test with ID: {postgrad_test.id}')
    else:
        print(f'Postgraduation test already exists with ID: {postgrad_test.id}')

    # Create Job Test
    job_test, created = PsychometricTest.objects.get_or_create(
        category='job',
        title='Career Job Selection Test',
        defaults={
            'description': 'Helps job seekers find the right career path based on their skills and preferences'
        }
    )

    if created:
        # Sample questions for job test
        job_questions = [
            {
                'text': 'What type of work schedule do you prefer?',
                'type': 'single_choice',
                'options': [
                    ('Regular 9-5 schedule', 2),
                    ('Flexible hours', 3),
                    ('Project-based work', 2),
                    ('Shift work', 1)
                ]
            },
            {
                'text': 'How important is work-life balance to you?',
                'type': 'scale',
                'options': []
            }
        ]

        for i, q_data in enumerate(job_questions):
            question = Question.objects.create(
                test=job_test,
                question_text=q_data['text'],
                question_type=q_data['type'],
                order=i + 1
            )
            
            for option_text, value in q_data['options']:
                AnswerOption.objects.create(
                    question=question,
                    option_text=option_text,
                    value=value,
                    order=len(question.answer_options.all()) + 1
                )

        print(f'Created job test with ID: {job_test.id}')
    else:
        print(f'Job test already exists with ID: {job_test.id}')

    print('\nTest Summary:')
    print(f'Graduation Test ID: {grad_test.id}')
    print(f'Post Graduation Test ID: {postgrad_test.id}')
    print(f'Job Test ID: {job_test.id}')

if __name__ == '__main__':
    create_sample_tests()
