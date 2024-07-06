
import boto3
import psycopg2
from psycopg2.extras import RealDictCursor

class GetConnection:
    def get_connection():
        return psycopg2.connect(
            host='localhost',
            port='5432',
            user='postgres',
            password='1234',
            dbname='Jobscript'
        )
