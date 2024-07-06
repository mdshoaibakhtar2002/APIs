from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import boto3
import psycopg2
from psycopg2.extras import RealDictCursor


class UserHelper(APIView):
    def get_connection():
        return psycopg2.connect(
            host='localhost',
            port='5432',
            user='postgres',
            password='1234',
            dbname='Jobscript'
        )

    def fetch_user():
        connection = UserHelper.get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute("SELECT * FROM users")
            data = cursor.fetchall()
            list_of_users = []
            if data:
                for i in data:
                    users = {}
                    for key, value in i.items():
                        users[key] = value
                    list_of_users.append(users)
                return list_of_users
        except Exception as e:
            connection.rollback()
            raise e

        finally:
            cursor.close()
            connection.close()


class UserManagement(APIView):
    def get(self, request, *args, **kwargs):
        data = UserHelper.fetch_user()
        return Response(
            {
                'statusCode': status.HTTP_200_OK,
                'result': data
            },
            status=status.HTTP_200_OK
        )
