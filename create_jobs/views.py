from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from psycopg2.extras import RealDictCursor
from utils.get_connection import GetConnection
import psycopg2
from utils.token_management import TokenManagement


class JobCreatorHandler(APIView):
    def post(self, request, *args, **kwargs):
        connection = GetConnection.get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        data = request.data

        query = """
            INSERT INTO jobs (
                job_role, 
                job_description,
                company_name,
                job_location,
                work_mode,
                job_offer,
                job_id,
                requirements,
                job_type,
                experience, 
                last_date, 
                skills,
                key_responsibilities,
                preferred_qualifications,
                immediate_joining
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        print('data',data)
        cursor.execute(query, (
            data['job_role'],
            data['job_description'],
            data['company_name'],
            data['job_location'],
            data['work_mode'],
            data['job_offer'],
            data['job_id'],
            data['requirements'],
            data['job_type'],
            data['experience'],
            data['last_date'],
            data['skills'],
            data['key_responsibilities'],
            data['preferred_qualifications'],
            data['immediate_joining']
        ))

        connection.commit()
        return Response(
            {
                'statusCode': status.HTTP_200_OK,
                'result': 'Job created successfully'
            },
            status=status.HTTP_200_OK
        )

    def get(self, request, *args, **kwargs):
        connection = GetConnection.get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM jobs")
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

