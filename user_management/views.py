from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from psycopg2.extras import RealDictCursor
from utils.get_connection import GetConnection
import psycopg2
from utils.token_management import TokenManagement


class UserManagement(APIView):
    def get(self, request, *args, **kwargs):
        connection = GetConnection.get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        list_of_users = []
        if data:
            for i in data:
                users = {}
                for key, value in i.items():
                    users[key] = value
                list_of_users.append(users)
        return Response(
            {
                'statusCode': status.HTTP_200_OK,
                'result': list_of_users
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        connection = GetConnection.get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        data = request.data

        query = """
            INSERT INTO users (email, phone_number, first_name, last_name,is_organization, password, confirm_password)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            data['email'],
            data['phone_number'],
            data['first_name'],
            data['last_name'],
            data['is_organization'],
            data['password'],
            data['confirm_password']
        ))

        connection.commit()
        return Response(
            {
                'statusCode': status.HTTP_200_OK,
                'result': 'User created successfully'
            },
            status=status.HTTP_200_OK
        )


class AuthenticateUser(APIView):
    def post(self, request, *args, **kwargs):
        connection = GetConnection.get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        data = request.data

        try:
            if not data.get('email') or not data.get('password'):
                return Response({
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'error': 'Email and password are required.'
                })

            cursor.execute(
                "SELECT * FROM users WHERE email = %s", (data['email'],))
            user = cursor.fetchone()

            if user is None:
                return Response({
                    'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'error': 'User not found.'
                })

            users = {key: value for key, value in user.items()}

            if data['password'] != users['password']:
                return Response({
                    'statusCode': status.HTTP_401_UNAUTHORIZED,
                    'error': 'Invalid email or password.'
                })

            if user['email'] is not None:
                print('Valid user, Now generating token...')
                token = TokenManagement.token_management(user['email'])
                print('token', token)
            return Response({
                'statusCode': status.HTTP_200_OK,
                'message': 'User authenticated successfully',
                'token': token,
                'data': {
                    'email': user['email'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name']
                }
            })

        except Exception as e:
            return Response({
                'statusCode': 500,
                'error': str(e)
            })
        finally:
            connection.close()
