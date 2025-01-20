"""
This module handles authentication and authorization using Auth0.
It includes functions to get the token from the authorization header,
verify and decode JWT tokens, and check permissions.
"""

import json
import os
import ssl
from functools import wraps
from urllib.request import urlopen
from flask import request
from jose import jwt
import certifi

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = os.getenv('AUTH0_ALGORITHMS', 'RS256').split(',')
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')

class AuthError(Exception):
    """
    Custom exception class for authentication errors.

    Attributes:
        error (dict): The error details.
        status_code (int): The HTTP status code.
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header():
    """
    Obtains the Access Token from the Authorization Header.

    Raises:
        AuthError: If the authorization header is missing or invalid.

    Returns:
        str: The token from the Authorization header.
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)
    if len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)
    if len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token

def verify_decode_jwt(token):
    """
    Verifies and decodes a JWT token.

    Args:
        token (str): The JWT token to be verified and decoded.

    Raises:
        AuthError: If the token is invalid or expired.

    Returns:
        dict: The decoded token payload.
    """
    if os.getenv('FLASK_ENV') == 'testing':
        # Load the public key for testing
        with open('tests/public_key.pem', 'r', encoding='utf-8') as f:
            public_key = f.read()
        try:
            payload = jwt.decode(token, public_key, algorithms=['RS256'])
            return payload
        except jwt.ExpiredSignatureError as exc:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token is expired.'
            }, 401) from exc
        except jwt.JWTClaimsError as exc:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401) from exc
        except Exception as exc:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 401) from exc
    else:
      ssl_context = ssl.create_default_context(cafile=certifi.where())
      with urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json', context=ssl_context) as jsonurl:
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
          try:
              payload = jwt.decode(
                  token,
                  rsa_key,
                  algorithms=ALGORITHMS,
                  audience=AUTH0_AUDIENCE,
                  issuer='https://' + AUTH0_DOMAIN + '/'
              )
              return payload

          except jwt.ExpiredSignatureError as exc:
              raise AuthError({
                  'code': 'token_expired',
                  'description': 'Token is expired.'
              }, 401) from exc
          except jwt.JWTClaimsError as exc:
              raise AuthError({
                  'code': 'invalid_claims',
                  'description': 'Incorrect claims. Please, check the audience and issuer.'
              }, 401) from exc
          except Exception as exc:
              raise AuthError({
                  'code': 'invalid_header',
                  'description': 'Unable to parse authentication token.'
              }, 401) from exc
      raise AuthError({
          'code': 'invalid_header',
          'description': 'Unable to find the appropriate key.'
      }, 400)

def check_permissions(permission, payload):
    """
    Checks if the required permission is present in the JWT payload.

    Args:
        permission (str): The required permission.
        payload (dict): The JWT payload.

    Raises:
        AuthError: If the required permission is not found in the payload.

    Returns:
        bool: True if the permission is found, False otherwise.
    """
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True

def requires_auth(permission=''):
    """
    Decorator function to enforce authentication on endpoints.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, payload=payload, **kwargs)

        return wrapper
    return requires_auth_decorator
