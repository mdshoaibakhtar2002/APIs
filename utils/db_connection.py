import json
import boto3
import psycopg2
from psycopg2.extras import RealDictCursor

# Define constants for the Secrets Manager and RDS proxy URL
SM_EXAMPLE_DATABASE_CREDENTIALS = 'rds!cluster-b2eed415-4dc5-4459-8662-28a431ed2ccf'
URL_RDS_PROXY = 'pocdatabse-instance-1.ctoue0wuiu87.us-west-2.rds.amazonaws.com'

# Uncomment and implement the following function if you need to retrieve credentials from AWS Secrets Manager
# def get_db_credentials():
#     secrets_manager = boto3.client('secretsmanager')
#     secret_value = secrets_manager.get_secret_value(SecretId=SM_EXAMPLE_DATABASE_CREDENTIALS)
#     print('secret_value', secret_value)
#     return json.loads(secret_value['SecretString'])


def get_connection():
    # Replace the following line with the actual function to get credentials if needed
    # credentials = get_db_credentials()
    print('credentials')
    return psycopg2.connect(
        host='localhost',
        port='5432',
        user='postgres',
        password='1234',
        dbname='test_db'
    )


def lambda_handler(event, context):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    print('Here All checks passed')

    try:
        cursor.execute("SELECT * FROM test_table")
        data = cursor.fetchone()
        print(data)
    except Exception as e:
        connection.rollback()
        raise e

    finally:
        # cursor.close()
        connection.close()


if __name__ == '__main__':
    # Example event and context for testing the lambda_handler function
    event = {}
    context = {}
    lambda_handler(event, context)
