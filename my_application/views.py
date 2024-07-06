from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class Test_API(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print('Hello data is here', data)
        return Response(
                {
                    'statusCode': status.HTTP_200_OK,
                    'data': data
                },
                status=status.HTTP_200_OK
            )

    def get(self, request, *args, **kwargs):
        print('Hello here')
        return Response(
                {
                    'statusCode': status.HTTP_200_OK,
                    'result':'I am here'
                },
                status=status.HTTP_200_OK
            )