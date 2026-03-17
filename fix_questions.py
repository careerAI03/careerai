#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careersai.settings')
django.setup()

from core.models import Question

# Update questions with appropriate traits
updates = [
    (121, 'business'),  # uncertainty and risk -> business
    (122, 'business'),  # industry excitement -> business  
    (123, 'social'),    # teaching/mentoring -> social
    (124, 'analytical'), # law/legal -> analytical
    (125, 'creative'),  # structured/flexible -> creative
    (126, 'social'),    # social impact -> social
    (127, 'business'),  # traveling for work -> business
    (128, 'technical'), # new technologies -> technical
    (129, 'analytical'), # learning motivation -> analytical
]

print("Updating questions with None trait values...")
for question_id, trait in updates:
    Question.objects.filter(id=question_id).update(trait=trait)
    print(f'Updated Question {question_id} to trait: {trait}')

print('All questions updated successfully!')

# Verify the update
remaining = Question.objects.filter(trait__isnull=True).count()
print(f'Remaining questions with None trait: {remaining}')
