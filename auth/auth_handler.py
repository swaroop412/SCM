import os
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta, timezone

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
print(SECRET_KEY)
if SECRET_KEY is None:
    raise ValueError("JWT key is not set in environment variables")
def sign_jwt(user_id: str, role:str,name:str) :
    payload = {
        "user_id": user_id,
        "role":role,
        "name":name,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256") # type: ignore
    return {"access_token": token}

def decode_jwt(token: str) -> dict:
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]) # type: ignore
        return decoded
    
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
    
