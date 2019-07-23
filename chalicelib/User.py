from chalicelib.Model import DynamoDBModel
import os
import boto3

class User(DynamoDBModel):

    _table = os.environ.get('USER_TABLE') or "user-dev"
    _partition_key = "username"

    def __init__(self, **params):
        if all(k in params for k in ('username', 'first_name', 'last_name', 'email')):
            self._username = params['username']
            self._first_name = params['first_name']
            self._last_name = params['last_name']
            self._email = params['email']
            self._hash = params['hash']
            self._hashed = params['hashed']
            self._salt = params['salt']
            self._rounds = params['rounds']
        else:
            raise ValueError("User must include: username, first name, last name, and email")
    
    def save(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(User._table)
        table.put_item(
            Item = {
                "username": self._username,
                "first_name": self._first_name,
                "last_name": self._last_name,
                "email": self._email,
                "hash": self._hash,
                "hashed": self._hashed,
                "salt": self._salt,
                "rounds": self._rounds
            },
            ConditionExpression=f'attribute_not_exists({User._partition_key}) or attribute_not_exists(email)'
        )
    
    @staticmethod
    def get(username):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(User._table)
        record = table.get_item(Key={f'{User._partition_key}': username})['Item']
        return User(**record)
    
    @property
    def username(self):
        return self._username
    
    @property
    def first_name(self):
        return self._first_name
    
    @property
    def last_name(self):
        return self._last_name
    
    @property
    def email(self):
        return self._email
    
    @property
    def hash(self):
        return self._hash

    @property
    def hashed(self):
        return self._hashed
    
    @property
    def salt(self):
        return self._salt
    
    @property
    def rounds(self):
        return self._rounds