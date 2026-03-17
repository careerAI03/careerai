# CareersAI - Psychometric Test Platform

A comprehensive Django-based platform for career guidance through psychometric testing.

## Features

- **User Authentication**: Email-based registration with OTP verification
- **Psychometric Tests**: Three categories of tests (Graduation, Post-Graduation, Job Career)
- **Random Question Selection**: 20 random questions per test attempt
- **Smart Recommendations**: AI-powered career suggestions based on test results
- **User Profiles**: Complete profile management with career history
- **Email Integration**: SMTP-based email notifications
- **REST API**: Full REST API with JWT authentication

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd careersai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   - Copy `.env` file and configure your settings:
     ```env
     SECRET_KEY=your-secret-key-here
     EMAIL_HOST=smtp.gmail.com
     EMAIL_PORT=587
     EMAIL_HOST_USER=your-email@gmail.com
     EMAIL_HOST_PASSWORD=your-app-password
     ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Populate Questions**
   ```bash
   python manage.py populate_questions
   ```

8. **Run Server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/core/auth/register/` - User registration
- `POST /api/core/auth/verify-otp/` - OTP verification
- `POST /api/core/auth/login/` - User login

### Profile
- `GET /api/core/profile/` - Get user profile
- `PUT /api/core/profile/` - Update user profile

### Tests
- `GET /api/core/tests/` - List all tests
- `POST /api/core/tests/start/` - Start a test
- `POST /api/core/tests/submit-answer/` - Submit answer
- `POST /api/core/tests/complete/` - Complete test
- `GET /api/core/tests/history/` - Test history

### Career
- `GET /api/core/career/recommendations/` - Get career recommendations

## Test Categories

1. **Graduation Stream Assessment** (50 questions)
   - Determines suitable undergraduate streams
   - Covers Science, Commerce, Arts, and other fields

2. **Post Graduation Assessment** (50 questions)
   - Recommends post-graduate programs
   - Includes MBA, M.Tech, MS, and other options

3. **Career Path Assessment** (50 questions)
   - Suggests job roles and career paths
   - Based on skills, interests, and personality

## Test Flow

1. User registers with email
2. OTP verification sent to email
3. User logs in and starts a test
4. 20 random questions selected from the category
5. User answers questions one by one
6. Test completed and results generated
7. Career recommendations provided based on scores

## Admin Panel

Access admin panel at `/admin/` with superuser credentials to:
- Manage users and tests
- View test results and statistics
- Add/modify questions and answers
- Monitor user activity

## Technology Stack

- **Backend**: Django 5.2
- **API**: Django REST Framework
- **Authentication**: JWT tokens
- **Database**: SQLite (development), PostgreSQL (production)
- **Email**: SMTP integration
- **File Storage**: Django file system

## Security Features

- JWT-based authentication
- CORS configuration
- CSRF protection
- Email verification
- Password validation
- Secure file uploads

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and queries, please contact the development team.
