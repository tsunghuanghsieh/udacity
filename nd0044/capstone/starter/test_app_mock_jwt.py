from cryptography.hazmat.primitives.asymmetric import rsa
import jwt
from jwt.utils import to_base64url_uint

# Algorithm used in Auth0
ALGORITHM = "RS256"
# "kid" in one of the two jwks from https://fsdcapstone.us.auth0.com/.well-known/jwks.json
PUBLIC_KEY_ID = "b7i5eVyKpjISn9nBLwo2-"

def generate_public_private_key_pair():
  private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
  public_key = private_key.public_key()
  return (public_key, private_key)

(public_key, private_key) = generate_public_private_key_pair()

def encode_token(payload):
  return jwt.encode(
    payload=payload,
    key=private_key,
    algorithm=ALGORITHM,
    headers=get_mock_jwk()
  )

def get_mock_user_claims(permissions):
  return {
    "iss": "https://fsdcapstone.us.auth0.com/",
    "sub": "auth0|62f804a7276e28eb38cf24cc",
    "aud": "casting",
    "iat": 1660985109,  # Issued on 08/20/2022
    "exp": 9999999999,  # One long-lasting token, expiring 11/20/2286
    "permissions": permissions,
  }

# Mock JWT token using self generated public/private key
def get_mock_token(permissions):
  return encode_token(get_mock_user_claims(permissions))

# Mock JWT token for Assistant role
def get_mock_assistant_token():
    return get_mock_token(permissions = [
        "get:actors",
        "get:auditions",
        "get:movies",
      ])

# Mock JWT token for Director role
def get_mock_director_token():
    return get_mock_token(permissions = [
        "delete:actors",
        "delete:auditions",
        "get:actors",
        "get:auditions",
        "get:movies",
        "patch:actors",
        "patch:auditions",
        "patch:movies",
        "post:actors",
        "post:auditions"
      ])

# Mock JWT token for Producer role
def get_mock_producer_token():
    return get_mock_token(permissions = [
        "delete:actors",
        "delete:auditions",
        "delete:movies",
        "get:actors",
        "get:auditions",
        "get:movies",
        "patch:actors",
        "patch:auditions",
        "patch:movies",
        "post:actors",
        "post:auditions",
        "post:movies"
      ])

# Mock JWK using self generated public key
def get_mock_jwk():
  public_numbers = public_key.public_numbers()

  return {
    "alg": ALGORITHM,
    "kid": PUBLIC_KEY_ID,
    "use": "sig",
    "kty": "RSA",
    "n": to_base64url_uint(public_numbers.n).decode("ascii"),
    "e": to_base64url_uint(public_numbers.e).decode("ascii"),
  }

# Mock JWKS returned from https://fsdcapstone.us.auth0.com/.well-known/jwks.json
def get_mock_jwks():
  return {
    "keys": [ get_mock_jwk() ]
  }
