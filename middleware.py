import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import Request, Depends, security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import security

bearer=HTTPBearer()
load_dotenv()
scret_key= os.getenv("secret_key")

def create_token(details:dict, expiry:int):
    expire= datetime.now() + timedelta(minutes=expiry)

    details.update({"exp":expire})
    # sign jwt
    encoder_jwt=jwt.encode(details, scret_key)
    return encoder_jwt

def verify_token(request: HTTPAuthorizationCredentials= Depends(bearer)):
    token= request.credentials
    verify_token=jwt.decode(token, scret_key, algorithms=["HS256"])
    # expiry_time= verify_token.get("exp")

    return{"email":verify_token.get("email"), "userType":verify_token.get("userType"), "id":verify_token.get("id")}