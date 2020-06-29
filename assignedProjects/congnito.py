from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
import boto3
import hmac
import hashlib
import base64
import uuid

USER_POOL_ID = 'us-east-1_x3Le9jtqC'
CLIENT_ID = '78s0cd1a802des8rbng7ehe9bm'
CLIENT_SECRET = 'm3mfo5eh51vt91nq6t8sofjpjto245t9ovhb1u21ef7n09s7ak'


def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def confirmemail(request):
    client = boto3.client('cognito-idp')
    username = 'amit.gupta+007@kiwitech.com'
    try:
        response = client.confirm_sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            ConfirmationCode='758236',
            ForceAliasCreation=False,
        )
    except client.exceptions.UserNotFoundException:
        return JsonResponse({"error": True, "success": False, "message": "Username doesnt exists"})
    except client.exceptions.CodeMismatchException:
        return JsonResponse({"error": True, "success": False, "message": "Invalid Verification code"})

    except client.exceptions.NotAuthorizedException:
        return JsonResponse({"error": True, "success": False, "message": "User is already confirmed"})

    except Exception as e:
        return JsonResponse({"error": True, "success": False, "message": f"Unknown error {e.__str__()} "})
    return JsonResponse({"error": False,
                         "success": True,
                         "message": "confirm"})


def signup(request):
    client = boto3.client('cognito-idp')
    username = 'amit.gupta+007@kiwitech.com'
    try:
        resp = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username='amit.gupta+007@kiwitech.com',
            Password='Fran@12345',
            UserAttributes=[
                {
                    'Name': "name",
                    'Value': 'Amit'
                },
                {
                    'Name': "email",
                    'Value': 'amit.gupta+007@kiwitech.com'
                }
            ],
            ValidationData=[
                {
                    'Name': "email",
                    'Value': "email"
                },
                {
                    'Name': "custom:username",
                    'Value': "username"
                }
            ]
        )

    except client.exceptions.UsernameExistsException as e:
        return JsonResponse({"error": False,
                             "success": True,
                             "message": "This username already exists",
                             "data": None})
    except client.exceptions.InvalidPasswordException as e:

        return JsonResponse({"error": False,
                             "success": True,
                             "message": "Password should have Caps,\
                          Special chars, Numbers",
                             "data": None})
    except client.exceptions.UserLambdaValidationException as e:
        return JsonResponse({"error": False,
                             "success": True,
                             "message": "Email already exists",
                             "data": None})

    except Exception as e:
        return JsonResponse({"error": False,
                             "success": True,
                             "message": str(e),
                             "data": None})

    return JsonResponse({"error": False,
                         "success": True,
                         "message": "Please confirm your signup, \
                        check Email for validation code",
                         "data": None})


def signin(request):
    client = boto3.client('cognito-idp')
    username = 'amit.gupta+007@kiwitech.com'
    password = 'Fran@12345'
    secret_hash = get_secret_hash(username)
    try:
        resp = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': secret_hash,
                'PASSWORD': password,
            },
            ClientMetadata={
                'username': username,
                'password': password,
            })
    except client.exceptions.NotAuthorizedException:
        return JsonResponse({"error": True,
                             "success": False,
                             "message": "The username or password is incorrect",
                             "data": None})
    except client.exceptions.UserNotConfirmedException:
        return JsonResponse({"error": True,
                             "success": False,
                             "message": "User is not confirmed",
                             "data": None})
    except Exception as e:
        return JsonResponse({"error": True,
                             "success": False,
                             "message": e.__str__(),
                             "data": None})
        return None, e.__str__()
    return JsonResponse({"error": False,
                         "success": True,
                         "message": resp,
                         "data": None})