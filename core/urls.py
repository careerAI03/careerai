from django.urls import path
from . import views

urlpatterns = [
    # Template Views
    path('', views.HomeView.as_view(), name='home'),
    path('auth/', views.AuthView.as_view(), name='auth'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('verify-otp/', views.TemplateView.as_view(template_name='verify_otp.html'), name='verify-otp'),
    path('test/', views.TestView.as_view(), name='test'),
    path('results/', views.ResultsView.as_view(), name='results'),
    path('logout/', views.logout_view, name='logout'),
    
    # API URLs
    path('api/core/auth/check-email/', views.CheckEmailView.as_view(), name='check-email'),
    path('api/core/auth/send-otp/', views.SendOTPView.as_view(), name='send-otp'),
    path('api/core/auth/verify-otp/', views.VerifyOTPView.as_view(), name='verify-otp-api'),
    path('api/core/auth/register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('api/core/auth/otp-verification/', views.OTPVerificationView.as_view(), name='otp-verification'),
    path('api/core/auth/login/', views.UserLoginView.as_view(), name='user-login'),
    path('api/core/auth/login-otp/', views.OTPLoginView.as_view(), name='otp-login'),
    
    # Profile URLs
    path('api/core/profile/', views.UserProfileView.as_view(), name='user-profile'),
    
    # Test URLs
    path('api/core/tests/', views.PsychometricTestListView.as_view(), name='test-list'),
    path('api/core/tests/start/', views.StartTestView.as_view(), name='start-test'),
    path('api/core/tests/submit-answer/', views.SubmitAnswerView.as_view(), name='submit-answer'),
    path('api/core/tests/complete/', views.CompleteTestView.as_view(), name='complete-test'),
    path('api/core/tests/history/', views.UserTestHistoryView.as_view(), name='test-history'),
    
    # Career URLs
    path('api/core/career/recommendations/', views.CareerRecommendationView.as_view(), name='career-recommendations'),
]
