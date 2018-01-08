import jwt
import datetime


def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.utcnow() + datetime.timedelta(days=0, minutes=1),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            'SECRET_KEY',
            algorithm='HS256'
        )

    except Exception as e:
        return e


def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, 'SECRET_KEY')
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
