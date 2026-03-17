from django.core.management.base import BaseCommand
from core.models import PsychometricTest, Question, AnswerOption

class Command(BaseCommand):
    help = 'Populate 120 questions (20 per field) with yes/no and knowledge questions'

    def handle(self, *args, **options):
        # Clear existing questions
        Question.objects.all().delete()
        AnswerOption.objects.all().delete()
        
        # Get or create test
        test, created = PsychometricTest.objects.get_or_create(
            category='graduation',
            defaults={
                'title': 'Comprehensive Career Assessment Test',
                'description': '120 questions across 6 fields to determine your career path'
            }
        )
        
        questions_data = {
            'technical': {
                'yes_no': [
                    "Do you enjoy programming and coding?",
                    "Are you interested in how computers work internally?",
                    "Do you like solving technical problems?",
                    "Are you fascinated by artificial intelligence?",
                    "Do you enjoy working with databases?",
                    "Are you interested in cybersecurity?",
                    "Do you like building and fixing computers?",
                    "Are you curious about cloud computing?",
                    "Do you enjoy learning programming languages?",
                    "Are you interested in software development?"
                ],
                'knowledge': [
                    "What does HTML stand for?",
                    "What is a CPU in a computer?",
                    "What is the purpose of an operating system?",
                    "What is RAM used for in computers?",
                    "What does 'API' stand for?",
                    "What is a database?",
                    "What is the function of a motherboard?",
                    "What is cloud storage?",
                    "What is a programming language?",
                    "What is the internet?"
                ]
            },
            'analytical': {
                'yes_no': [
                    "Do you enjoy solving mathematical problems?",
                    "Are you good at pattern recognition?",
                    "Do you like working with statistics?",
                    "Are you interested in data analysis?",
                    "Do you enjoy logical reasoning?",
                    "Are you good at finding errors in data?",
                    "Do you like research and investigation?",
                    "Are you interested in financial analysis?",
                    "Do you enjoy optimization problems?",
                    "Are you good at critical thinking?"
                ],
                'knowledge': [
                    "What is the average of 10, 20, 30?",
                    "What is 15% of 200?",
                    "What is a hypothesis in research?",
                    "What is a variable in mathematics?",
                    "What is probability?",
                    "What is a statistical mean?",
                    "What is algebra?",
                    "What is a data set?",
                    "What is correlation?",
                    "What is a logical statement?"
                ]
            },
            'creative': {
                'yes_no': [
                    "Do you enjoy drawing or painting?",
                    "Are you interested in graphic design?",
                    "Do you like creative writing?",
                    "Are you fascinated by visual arts?",
                    "Do you enjoy photography?",
                    "Are you interested in fashion design?",
                    "Do you like music composition?",
                    "Are you good at brainstorming ideas?",
                    "Do you enjoy interior design?",
                    "Are you interested in animation?"
                ],
                'knowledge': [
                    "What are the primary colors?",
                    "What is the golden ratio in design?",
                    "What is typography?",
                    "What is a color wheel?",
                    "What is composition in art?",
                    "What is perspective in drawing?",
                    "What is branding?",
                    "What is user experience (UX)?",
                    "What is a design principle?",
                    "What is visual hierarchy?"
                ]
            },
            'business': {
                'yes_no': [
                    "Do you enjoy leadership roles?",
                    "Are you interested in entrepreneurship?",
                    "Do you like managing projects?",
                    "Are you good at negotiation?",
                    "Do you enjoy marketing activities?",
                    "Are you interested in finance?",
                    "Do you like strategic planning?",
                    "Are you good at public speaking?",
                    "Do you enjoy networking?",
                    "Are you interested in business management?"
                ],
                'knowledge': [
                    "What is a business plan?",
                    "What is profit in business?",
                    "What is marketing?",
                    "What is a balance sheet?",
                    "What is revenue?",
                    "What is a target market?",
                    "What is supply and demand?",
                    "What is investment?",
                    "What is a competitor?",
                    "What is a business strategy?"
                ]
            },
            'social': {
                'yes_no': [
                    "Do you enjoy helping others?",
                    "Are you good at counseling people?",
                    "Do you like teaching?",
                    "Are you interested in psychology?",
                    "Do you enjoy community service?",
                    "Are you good at communication?",
                    "Do you like social work?",
                    "Are you interested in human behavior?",
                    "Do you enjoy mentoring others?",
                    "Are you good at conflict resolution?"
                ],
                'knowledge': [
                    "What is empathy?",
                    "What is social work?",
                    "What is counseling?",
                    "What is community development?",
                    "What is human psychology?",
                    "What is social justice?",
                    "What is communication?",
                    "What is group dynamics?",
                    "What is social behavior?",
                    "What is emotional intelligence?"
                ]
            },
            'medical': {
                'yes_no': [
                    "Do you enjoy biology?",
                    "Are you interested in human anatomy?",
                    "Do you like helping sick people?",
                    "Are you fascinated by medicine?",
                    "Do you enjoy chemistry?",
                    "Are you interested in healthcare?",
                    "Do you like research in life sciences?",
                    "Are you good at handling emergencies?",
                    "Do you enjoy patient care?",
                    "Are you interested in medical technology?"
                ],
                'knowledge': [
                    "What is DNA?",
                    "What is a cell?",
                    "What is the human heart?",
                    "What is blood circulation?",
                    "What are bacteria?",
                    "What is vaccination?",
                    "What is first aid?",
                    "What is nutrition?",
                    "What is the immune system?",
                    "What is a virus?"
                ]
            }
        }
        
        # Answers for knowledge questions
        knowledge_answers = {
            'technical': [
                {
                    'question': "What does HTML stand for?",
                    'correct': "HyperText Markup Language",
                    'incorrect': ["High Tech Modern Language", "Home Tool Markup Language", "Hyperlink and Text Markup Language"]
                },
                {
                    'question': "What is a CPU in a computer?",
                    'correct': "Central Processing Unit",
                    'incorrect': ["Computer Processing Unit", "Central Program Unit", "Core Processing Unit"]
                },
                {
                    'question': "What is the purpose of an operating system?",
                    'correct': "Manages computer hardware and software",
                    'incorrect': ["Only runs applications", "Provides internet connection", "Stores files only"]
                },
                {
                    'question': "What is RAM used for in computers?",
                    'correct': "Temporary memory storage",
                    'incorrect': ["Permanent storage", "Processing calculations", "Display output"]
                },
                {
                    'question': "What does 'API' stand for?",
                    'correct': "Application Programming Interface",
                    'incorrect': ["Advanced Programming Interface", "Application Process Interface", "Automated Programming Interface"]
                },
                {
                    'question': "What is a database?",
                    'correct': "Organized collection of data",
                    'incorrect': ["Programming language", "Software application", "Network protocol"]
                },
                {
                    'question': "What is the function of a motherboard?",
                    'correct': "Main circuit board",
                    'incorrect': ["Storage device", "Processing unit", "Memory module"]
                },
                {
                    'question': "What is cloud storage?",
                    'correct': "Online file storage",
                    'incorrect': ["Local hard drive", "Computer memory", "USB storage"]
                },
                {
                    'question': "What is a programming language?",
                    'correct': "Instructions for computers",
                    'incorrect': ["Database system", "Network protocol", "Operating system"]
                },
                {
                    'question': "What is the internet?",
                    'correct': "Global network of computers",
                    'incorrect': ["Single computer system", "Local network", "Software program"]
                }
            ],
            'analytical': [
                {
                    'question': "What is the average of 10, 20, 30?",
                    'correct': "20",
                    'incorrect': ["15", "25", "30"]
                },
                {
                    'question': "What is 15% of 200?",
                    'correct': "30",
                    'incorrect': ["20", "25", "35"]
                },
                {
                    'question': "What is a hypothesis in research?",
                    'correct': "A proposed explanation",
                    'incorrect': ["A final conclusion", "A research method", "A data collection tool"]
                },
                {
                    'question': "What is a variable in mathematics?",
                    'correct': "A symbol representing value",
                    'incorrect': ["A constant number", "A formula", "A calculation result"]
                },
                {
                    'question': "What is probability?",
                    'correct': "Likelihood of an event",
                    'incorrect': ["Certainty of outcome", "Random guess", "Statistical average"]
                },
                {
                    'question': "What is a statistical mean?",
                    'correct': "Average of data points",
                    'incorrect': ["Middle value", "Most frequent value", "Range of values"]
                },
                {
                    'question': "What is algebra?",
                    'correct': "Mathematical study of symbols",
                    'incorrect': ["Study of numbers only", "Geometry study", "Statistics branch"]
                },
                {
                    'question': "What is a data set?",
                    'correct': "Collection of data values",
                    'incorrect': ["Single data point", "Data analysis method", "Graph representation"]
                },
                {
                    'question': "What is correlation?",
                    'correct': "Relationship between variables",
                    'incorrect': ["Causation effect", "Random association", "Data collection method"]
                },
                {
                    'question': "What is a logical statement?",
                    'correct': "Statement that can be true or false",
                    'incorrect': ["Question", "Command", "Expression"]
                }
            ],
            'creative': [
                {
                    'question': "What are the primary colors?",
                    'correct': "Red, Blue, Yellow",
                    'incorrect': ["Red, Green, Blue", "Black, White, Gray", "Orange, Purple, Green"]
                },
                {
                    'question': "What is the golden ratio in design?",
                    'correct': "Mathematical proportion",
                    'incorrect': ["Color scheme", "Font style", "Layout grid"]
                },
                {
                    'question': "What is typography?",
                    'correct': "Art of arranging text",
                    'incorrect': ["Color selection", "Image editing", "Video production"]
                },
                {
                    'question': "What is a color wheel?",
                    'correct': "Circle of colors",
                    'incorrect': ["Color palette", "Paint brush", "Design software"]
                },
                {
                    'question': "What is composition in art?",
                    'correct': "Arrangement of elements",
                    'incorrect': ["Color mixing", "Brush technique", "Frame selection"]
                },
                {
                    'question': "What is perspective in drawing?",
                    'correct': "3D representation technique",
                    'incorrect': ["Color shading", "Line thickness", "Paper texture"]
                },
                {
                    'question': "What is branding?",
                    'correct': "Creating company identity",
                    'incorrect': ["Product packaging", "Advertising campaign", "Sales strategy"]
                },
                {
                    'question': "What is user experience (UX)?",
                    'correct': "User interaction design",
                    'incorrect': ["Graphic design", "Web development", "Content writing"]
                },
                {
                    'question': "What is a design principle?",
                    'correct': "Fundamental design rule",
                    'incorrect': ["Design software", "Design trend", "Design project"]
                },
                {
                    'question': "What is visual hierarchy?",
                    'correct': "Visual importance order",
                    'incorrect': ["Color arrangement", "Size variation", "Layout structure"]
                }
            ],
            'business': [
                {
                    'question': "What is a business plan?",
                    'correct': "Document outlining business goals",
                    'incorrect': ["Marketing strategy", "Financial report", "Employee handbook"]
                },
                {
                    'question': "What is profit in business?",
                    'correct': "Revenue minus expenses",
                    'incorrect': ["Total revenue", "Sales amount", "Investment return"]
                },
                {
                    'question': "What is marketing?",
                    'correct': "Promoting products/services",
                    'incorrect': ["Manufacturing goods", "Hiring employees", "Accounting records"]
                },
                {
                    'question': "What is a balance sheet?",
                    'correct': "Financial statement",
                    'incorrect': ["Marketing plan", "Sales report", "Employee schedule"]
                },
                {
                    'question': "What is revenue?",
                    'correct': "Total income",
                    'incorrect': ["Net profit", "Operating cost", "Investment capital"]
                },
                {
                    'question': "What is a target market?",
                    'correct': "Specific customer group",
                    'incorrect': ["All customers", "Competitor market", "Global market"]
                },
                {
                    'question': "What is supply and demand?",
                    'correct': "Economic principle",
                    'incorrect': ["Marketing strategy", "Financial ratio", "Business model"]
                },
                {
                    'question': "What is investment?",
                    'correct': "Putting money into ventures",
                    'incorrect': ["Spending money", "Saving money", "Borrowing money"]
                },
                {
                    'question': "What is a competitor?",
                    'correct': "Other businesses in same market",
                    'incorrect': ["Business partner", "Customer", "Supplier"]
                },
                {
                    'question': "What is a business strategy?",
                    'correct': "Plan to achieve goals",
                    'incorrect': ["Daily operations", "Employee training", "Office layout"]
                }
            ],
            'social': [
                {
                    'question': "What is empathy?",
                    'correct': "Understanding others' feelings",
                    'incorrect': ["Ignoring emotions", "Giving advice", "Being sympathetic"]
                },
                {
                    'question': "What is social work?",
                    'correct': "Helping community members",
                    'incorrect': ["Office administration", "Financial management", "Technical support"]
                },
                {
                    'question': "What is counseling?",
                    'correct': "Guiding people through problems",
                    'incorrect': ["Giving orders", "Medical treatment", "Legal advice"]
                },
                {
                    'question': "What is community development?",
                    'correct': "Improving local communities",
                    'incorrect': ["Building houses", "Creating businesses", "Marketing products"]
                },
                {
                    'question': "What is human psychology?",
                    'correct': "Study of human mind",
                    'incorrect': ["Physical health", "Social behavior", "Cultural traditions"]
                },
                {
                    'question': "What is social justice?",
                    'correct': "Fair treatment for all",
                    'incorrect': ["Legal system", "Economic equality", "Political power"]
                },
                {
                    'question': "What is communication?",
                    'correct': "Exchanging information",
                    'incorrect': ["Speaking only", "Writing only", "Listening only"]
                },
                {
                    'question': "What is group dynamics?",
                    'correct': "How groups interact",
                    'incorrect': ["Individual behavior", "Social media", "Family relationships"]
                },
                {
                    'question': "What is social behavior?",
                    'correct': "How people act together",
                    'incorrect': ["Personal habits", "Physical activities", "Mental processes"]
                },
                {
                    'question': "What is emotional intelligence?",
                    'correct': "Managing emotions",
                    'incorrect': ["Being emotional", "Logical thinking", "Social skills"]
                }
            ],
            'medical': [
                {
                    'question': "What is DNA?",
                    'correct': "Genetic material",
                    'incorrect': ["Protein", "Cell membrane", "Blood component"]
                },
                {
                    'question': "What is a cell?",
                    'correct': "Basic unit of life",
                    'incorrect': ["Organ", "Tissue", "Molecule"]
                },
                {
                    'question': "What is the human heart?",
                    'correct': "Pumping organ",
                    'incorrect': ["Filtering organ", "Digestive organ", "Breathing organ"]
                },
                {
                    'question': "What is blood circulation?",
                    'correct': "Blood movement in body",
                    'incorrect': ["Air flow in lungs", "Food digestion", "Nerve signals"]
                },
                {
                    'question': "What are bacteria?",
                    'correct': "Microorganisms",
                    'incorrect': ["Viruses", "Fungi", "Parasites"]
                },
                {
                    'question': "What is vaccination?",
                    'correct': "Disease prevention",
                    'incorrect': ["Disease treatment", "Symptom relief", "Pain management"]
                },
                {
                    'question': "What is first aid?",
                    'correct': "Emergency medical help",
                    'incorrect': ["Long-term treatment", "Surgery", "Diagnosis"]
                },
                {
                    'question': "What is nutrition?",
                    'correct': "Food and health",
                    'incorrect': ["Exercise", "Sleep", "Medication"]
                },
                {
                    'question': "What is the immune system?",
                    'correct': "Body defense system",
                    'incorrect': ["Digestive system", "Nervous system", "Circulatory system"]
                },
                {
                    'question': "What is a virus?",
                    'correct': "Microscopic agent",
                    'incorrect': ["Bacteria", "Cell", "Parasite"]
                }
            ]
        }
        
        question_counter = 0
        
        for field, field_data in questions_data.items():
            # Add yes/no questions
            for i, question_text in enumerate(field_data['yes_no']):
                question_counter += 1
                question = Question.objects.create(
                    test=test,
                    question_text=question_text,
                    question_type='yes_no',
                    field=field,
                    order=question_counter
                )
                
                # Create yes/no options
                AnswerOption.objects.create(
                    question=question,
                    option_text="Yes",
                    value=1,
                    order=1
                )
                AnswerOption.objects.create(
                    question=question,
                    option_text="No",
                    value=-1,
                    order=2
                )
            
            # Add knowledge questions
            for question_data in knowledge_answers[field]:
                question_counter += 1
                question = Question.objects.create(
                    test=test,
                    question_text=question_data['question'],
                    question_type='single_choice',
                    field=field,
                    order=question_counter
                )
                
                # Create correct answer
                AnswerOption.objects.create(
                    question=question,
                    option_text=question_data['correct'],
                    value=1,
                    order=1
                )
                
                # Create 3 incorrect answers
                for j, incorrect_answer in enumerate(question_data['incorrect']):
                    AnswerOption.objects.create(
                        question=question,
                        option_text=incorrect_answer,
                        value=-1,
                        order=j+2
                    )  
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {question_counter} questions across 6 fields')
        )
