import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'fsdcapstone.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'casting'

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
    auth_header = request.headers.get("Authorization", None)
    if auth_header is None:
        raise AuthError("Unauthorized: Missing Authorization Token", 401)
    auth_header_parts = auth_header.split(" ")
    if (len(auth_header_parts) != 2):
        raise AuthError("Bad Request: Malformed Authorization Token", 400)
    if (auth_header_parts[0].lower() != "bearer"):
        raise AuthError("Bad Request: No Bearer", 400)

    return auth_header_parts[1]

def check_permissions(permission, payload):
    if ("permissions" not in payload):
        raise AuthError("Bad Request: Permission Not In JWT", 400)
    if (permission not in payload["permissions"]):
        raise AuthError("Forbidden: No Required Permission", 403)

    return True

def verify_decode_jwt(token):
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if "kid" not in unverified_header:
        raise AuthError("Unauthorized: Unauthorized", 401)

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
            break
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://{}/".format(AUTH0_DOMAIN)
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError(": Token Expired", 401)
        except jwt.JWTClaimsError:
            raise AuthError(": Incorrect Claims", 401)
        except:
            raise AuthError(": Invalid Header", 400)
    raise AuthError(": No Matching Key", 400)

'''
@requires_auth(permission) decorator method
permission: specified in Auth0 API permission (https://manage.auth0.com/dashboard/us/fsdcapstone/apis/62f7ef76ecf63dc3e311d697/permissions)
            get:actors
            get:auditions
            get:movies
            post:actors
            post:auditions
            post:movies
            patch:actors
            patch:auditions
            patch:movies
            delete:actors
            delete:auditions
            delete:movies
'''
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