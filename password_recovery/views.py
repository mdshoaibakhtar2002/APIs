# accounts/views.py
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from .models import PasswordResetOTP
from .serializers import ForgotPasswordSerializer, OTPVerifySerializer, ResetPasswordSerializer

User = get_user_model()

class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            PasswordResetOTP.objects.create(user=user, otp=otp)
            message = Mail(
                from_email='your_email@example.com',
                to_emails=email,
                subject='Your OTP for Password Reset',
                html_content=f'Your OTP is {otp}'
            )
            sg = SendGridAPIClient(api_key='your_sendgrid_api_key')
            sg.send(message)
            return Response({'message': 'OTP sent to email'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(generics.GenericAPIView):
    serializer_class = OTPVerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        try:
            user = User.objects.get(email=email)
            otp_entry = PasswordResetOTP.objects.filter(user=user, otp=otp, created_at__gte=timezone.now()-timezone.timedelta(minutes=10)).first()
            if otp_entry:
                return Response({'message': 'OTP verified'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']
        try:
            user = User.objects.get(email=email)
            otp_entry = PasswordResetOTP.objects.filter(user=user, otp=otp, created_at__gte=timezone.now()-timezone.timedelta(minutes=10)).first()
            if otp_entry:
                user.set_password(new_password)
                user.save()
                otp_entry.delete()  # Optionally delete OTP entry after successful reset
                return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
