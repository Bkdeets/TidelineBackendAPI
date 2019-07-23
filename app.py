from chalice import Chalice, AuthResponse, Response
from chalicelib.User import User
from chalicelib.UserAuthUtility import UserAuthUtility
from boto3.dynamodb.types import Binary
from decimal import Decimal
import botocore
import json

app = Chalice(app_name='BackendApi')

STATUS_CODES = {
    "ConditionalCheckFailedException": 400,
    "Unknown": 502
}

@app.authorizer()
def jwt_auth(auth_request):
    token = auth_request.token
    print(token)
    decoded = UserAuthUtility.decode_jwt_token(token)
    return AuthResponse(routes=['*'], principal_id=decoded['sub'])

@app.route('/register', methods=['POST'])
def register():
    body = app.current_request.json_body
    username = body['username'].lower()
    password = body['password']
    first_name = body['first_name']
    last_name = body['last_name']
    email = body['email']
    try:
        password_fields = UserAuthUtility.encode_password(str.encode(password))
        user = User(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            hash = password_fields['hash'],
            salt = Binary(password_fields['salt']),
            rounds = password_fields['rounds'],
            hashed = Binary(password_fields['hashed'])
        )
        user.save()
    except botocore.exceptions.ClientError as e:
        raise e
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return Response(
                body='Username already exists',
                status_code=STATUS_CODES['ConditionalCheckFailedException']
            )
        else:
            return Response(
                body='Unknown error occurred',
                status_code=STATUS_CODES['Unknown']
            )
    except Exception as e:
        raise e
        return Response(
            body='Unknown error occurred',
            status_code=STATUS_CODES['Unknown']
        )
    else:
        return f"User username successfully registered"

@app.route('/login', methods=['POST'])
def login():
    body = app.current_request.json_body
    username = body['username']
    password = body['password']

    user = User.get(username)
    jwt_token = UserAuthUtility.get_jwt_token(
        user,
        password
    )
    return {'token': jwt_token}

@app.route('/hello', methods=['GET'], authorizer=jwt_auth)
def hello():
    UserAuthUtility.get_authorized_username(app.current_request)
    return {'hello': 'world'}