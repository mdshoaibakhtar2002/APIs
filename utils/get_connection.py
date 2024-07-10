
import boto3
import psycopg2
from psycopg2.extras import RealDictCursor

class GetConnection:
    def get_connection():
        return psycopg2.connect(
            host='ep-summer-pine-a4qfoktt-pooler.us-east-1.aws.neon.tech',
            port='5432',
            user='default',
            password='ugSBv0pUH4tC',
            dbname='verceldb'
        )
