from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from psycopg2.extras import RealDictCursor
from utils.get_connection import GetConnection
import psycopg2
import json
from utils.token_management import TokenManagement


class ApplyJob(APIView):
    def post(self, request, *args, **kwargs):
        connection = GetConnection.get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        data = request.data

        cursor.execute("SELECT job_id FROM users WHERE email = %s", (data['email'],))
        list_of_job_id = cursor.fetchall()
        updated_job_list = []
        if list_of_job_id:
            for i in list_of_job_id:
                for key, value in i.items():
                    updated_job_list = value
                    
        updated_job_list.append(data['job_id'])

        cursor.execute("UPDATE users SET job_id = %s WHERE email = %s", (updated_job_list,data['email'],))

        connection.commit()
        return Response(
            {
                'statusCode': status.HTTP_200_OK,
                'result': 'Applied successfully'
            },
            status=status.HTTP_200_OK
        )