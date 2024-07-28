# accounts/views.py
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.get_connection import GetConnection
from utils.send_otp import SendOTP
from psycopg2.extras import RealDictCursor
import psycopg2

class VerifyOTP(APIView):
    def post(self, request):
        connection = GetConnection.get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        data = request.data
        cursor.execute("SELECT otp FROM users WHERE phone_number = %s", (
            data['phone_number'],
        ))
        resp = cursor.fetchone()

        sent_otp = {key: value for key, value in resp.items()}
        otp = sent_otp.get('otp')
        if otp is None:
            return Response({
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'error': 'Please re-send otp'
            })
        
        if otp == 0:
            return Response({
                'status_code': status.HTTP_400_BAD_REQUEST,
                'error': 'OTP expired, Please try again.'
            })
            
        
        if(data.get('otp') == otp):
            SendOTP.expire_otp(data['phone_number'])
            return Response(
                {
                    'statud_code' : status.HTTP_200_OK,
                    'message' : 'OTP verified'
                },
                status = status.HTTP_200_OK
            )
            
        return Response(
                {
                    'statud_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Invalid OTP'
                },
                status = status.HTTP_400_BAD_REQUEST
            )
            
class ResetPassword(APIView):
    def post(self, request):
        connection = GetConnection.get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        data = request.data
        
        print('Data', data)
        
        if(data['password'] != data['confirm_password']):
            return Response(
                    {
                        'statud_code' : status.HTTP_400_BAD_REQUEST,
                        'message' : 'Password and Confirm password not matched'
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )
            
        cursor.execute("""UPDATE users SET password = %s, confirm_password = %s WHERE phone_number=%s""", (
            data['password'],
            data['confirm_password'],
            data['phone_number'],
        ))
        connection.commit()
        
        return Response(
                {
                    'statud_code' : status.HTTP_200_OK,
                    'message' : 'Successfully reset password.'
                },
                status = status.HTTP_200_OK
            )
        
class ForgotPassword(APIView):
    def post(self, request):
        data = request.data
        
        print('Data', data)
        
        send_otp = SendOTP.send_otp(data['phone_number']).__dict__
        otp_response = send_otp.get('data')
        
        if(otp_response.get('status_code') == 200):
            return Response(
                {
                    'statusCode': status.HTTP_200_OK,
                    'result': 'Sent OTP successfully'
                },
                status=status.HTTP_200_OK
            )
        
        
        return Response(
                {
                    'statud_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Please try again later.'
                },
                status = status.HTTP_400_BAD_REQUEST
            )