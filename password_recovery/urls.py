# accounts/urls.py
from django.urls import path
from .views import VerifyOTP, ResetPassword, ForgotPassword

urlpatterns = [
    path('verify-otp', VerifyOTP.as_view(), name='verify-otp'),
    path('reset-password', ResetPassword.as_view(), name='reset-password'),
    path('forgot-password', ForgotPassword.as_view(), name='forgot-password'),
]