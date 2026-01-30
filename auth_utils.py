from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime, timedelta

SECRET = "akjlfdhjkfaiefbcla;fh;ads;ifa;ihfs;aihdf;jknhueiafbvzb.zmv"
ALGORITHM = "HS256"
EXPIRY_TOKEN_TIME = 30


pwd_context = CryptContext(schemes=["argon2"],deprecated='auto')

def hashed_password(password: str):
    return pwd_context.hash(password)

def password_verification(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def createToken(data: dict, expiry_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expiry_delta if expiry_delta else timedelta(minutes=EXPIRY_TOKEN_TIME))
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET,algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token,SECRET,algorithms=ALGORITHM)
        return payload
    except JWTError:
        return None
