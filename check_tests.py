#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careersai.settings')
django.setup()

from core.models import PsychometricTest

print("=== Current Psychometric Tests ===")
tests = PsychometricTest.objects.all()
for test in tests:
    print(f"ID: {test.id}, Category: {test.category}, Title: {test.title}")

print("\n=== Categories ===")
categories = set(test.category for test in tests)
print(f"Available categories: {list(categories)}")
