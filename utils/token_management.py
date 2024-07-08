import jwt
import datetime

SECRET_KEY = 'your_secret_key_#123'

class TokenManagement:
    def token_management(user_email):
        print('Calling generate jwt')
        payload = {
            'email': user_email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration time
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        print('Generate token', token)
        return token