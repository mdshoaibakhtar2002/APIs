import json
import boto3
import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    # Replace the following line with the actual function to get credentials if needed
    # credentials = get_db_credentials()
    print('credentials')
    return psycopg2.connect(
        host='localhost',
        port='5432',
        user='postgres',
        password='1234',
        dbname='Jobscript'
    )


def lambda_handler(event, context):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    print('Here All checks passed')

    try:
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        arr = []
        if data:
            for i in data:
                obj = {}
                for key, value in i.items():
                    obj[key] = value

                arr.append(obj)
            print(arr)
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
