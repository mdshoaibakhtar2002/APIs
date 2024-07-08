from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from psycopg2.extras import RealDictCursor
from utils.get_connection import GetConnection
import psycopg2

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

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return Response(
                {
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'message': 'Email and password are required.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user is None:
                return Response(
                    {
                        'statusCode': status.HTTP_404_NOT_FOUND,
                        'message': 'User not found.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            users = {}
            for key, value in user.items():
                    users[key] = value

            # print('users', users)
            if password != users['password']:
                return Response(
                    {
                        'statusCode': status.HTTP_401_UNAUTHORIZED,
                        'message': 'Invalid password.'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            return Response(
                {
                    'statusCode': status.HTTP_200_OK,
                    'message': 'User authenticated successfully',
                    'data': {
                        'email': user['email'],
                        'first_name': user['first_name'],
                        'last_name': user['last_name']
                    }
                },
                status=status.HTTP_200_OK
            )

        except psycopg2.Error as e:
            return Response(
                {
                    'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Database error: ' + str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        finally:
            cursor.close()
            connection.close()
