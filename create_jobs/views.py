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
            INSERT INTO jobs (job_role, company_name, location, work_mode, job_offer, company_size, company_logo, start_date, experience, last_date, probation_period, skills, requirement, perks_benefit, eligibility, availabilty)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            data['job_role'],
            data['company_name'],
            data['location'],
            data['work_mode'],
            data['job_offer'],
            data['company_size'],
            data['company_logo'],
            data['start_date'],
            data['experience'],
            data['last_date'],
            data['probation_period'],
            data['skills'],
            data['requirement'],
            data['perks_benefit'],
            data['eligibility'],
            data['availabilty']
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

