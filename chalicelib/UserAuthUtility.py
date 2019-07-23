import datetime
import hashlib
import hmac
import json
import os
import base64
from uuid import uuid4

import boto3

import jwt
from chalice import UnauthorizedError
from chalicelib.User import User

_SECRET = 's$6W743zJOGy5^EQ8Q#Z47m%5'

class UserAuthUtility:

    @staticmethod
    def encode_password(password, salt=None):
        if not(salt):
            salt = os.urandom(16)
        rounds = 100000
        hashed = hashlib.pbkdf2_hmac('sha256', password, salt, rounds)
        return {
            'hash': 'sha256',
            'salt': salt,
            'rounds': rounds,
            'hashed': hashed
        }

    @staticmethod
    def get_authorized_username(current_request):
        return current_request.context['authorizer']['principalId']

    @staticmethod
    def get_jwt_token(user_obj, password):
        actual = hashlib.pbkdf2_hmac(
            user_obj.hash,
            str.encode(password),
            user_obj.salt.value,
            user_obj.rounds
        )
        expected = user_obj.hashed.value
        if hmac.compare_digest(actual, expected):
            now = datetime.datetime.utcnow()
            print(now)
            unique_id = str(uuid4())
            payload = {
                'sub': user_obj.username,
                'iat': now,
                'nbf': now,
                'jti': unique_id
                # NOTE: We can also add 'exp' if we want tokens to expire.
            }
            return jwt.encode(payload, _SECRET, 'HS256').decode('utf-8')
        raise UnauthorizedError('Invalid password')
    
    @staticmethod
    def decode_jwt_token(token):
        return jwt.decode(token, _SECRET, algorithms=['HS256'])
