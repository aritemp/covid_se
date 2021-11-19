import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# https://github.com/auth0-samples/auth0-python-api-samples/blob/master/00-Starter-Seed/server.py
# Practice - Validating Auth0 Tokens

AUTH0_DOMAIN = 'fwddev.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'se_covid2021'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    try:
        auth_header = request.headers.get('Authorization', None)

        if not auth_header:
            raise AuthError({
           'code': 'authorization_header_missing',
           'description': 'Authorization header is missing.',
       }, 401)

        header_parts = auth_header.split()

        if header_parts[0] == 'Bearer' and len(header_parts)==2:
            return header_parts[1]

        else:
            if header_parts[0] != 'Bearer':
                raise AuthError({
               "code": "invalid_header",
               "description": 'Authorization header must start with Bearer.'
                }, 401)

            elif len(header_parts) != 2:
                raise AuthError({
                "code": "invalid_header",
                "description": 'Authorization header is malformed.'
                    }, 400)
    except:
        abort(422)


def check_permissions(permission, payload):

    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT payload.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'missing_or_bad_authentication',
            'description': 'Permissions not found.'
        }, 401)

    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        #print(token)
        #print(API_AUDIENCE)
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please check the audience and issuer.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
