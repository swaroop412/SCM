from fastapi import APIRouter, HTTPException, Depends, Security
from auth.schemas import User, Login, Shipment
from auth.models import hash_password, verify_password
from auth.auth_handler import sign_jwt, decode_jwt
from pymongo.database import Database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from bson import ObjectId

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt(token)
    if "error" in payload:
        raise HTTPException(status_code=401, detail=payload["error"])
    return payload


def require_role(role: str):
    def role_dependency(user: dict = Depends(get_current_user)):
        if user.get("role") != role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_dependency




def auth_router(db: Database):
    router = APIRouter()

    @router.post("/signup")
    def signup(user: User):
        if db.users.find_one({"email": user.email}):
            raise HTTPException(status_code=400, detail="Email already registered")

        user_data = user.dict()
        user_data["password"] = hash_password(user.password)
        db.users.insert_one(user_data)
        return {"message": "User created successfully", "object_id": str(user_data["_id"]), "user_email":str(user_data["email"])}

    @router.post("/login")
    def login(user: Login):
        db_user = db.users.find_one({"email": user.email})
        if not db_user or not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return sign_jwt(user.email,db_user["role"])

    @router.post("/renew_token")
    def renew_token(token: str=Depends(oauth2_scheme)):
        payload = decode_jwt(token)
        if "error" in payload:
            raise HTTPException(status_code=401,detail=payload["error"])
        
        user_id = payload["user_id"]
        role = payload["role"]
        return sign_jwt(user_id,role)
    return router

def shipment_router(db: Database) -> APIRouter:
    router = APIRouter()
    @router.post("/create_shipment")
    def create_shipment(shipment: Shipment):
        
        try:
            shipment_data = shipment.dict(by_alias=True)
            shipment_data["expected_delivery_date"] = shipment_data["expected_delivery_date"].isoformat()
            db.shipments.insert_one(shipment_data)
            return {"message": "Shipment created successfully", "shipment_id": str(shipment_data["_id"])}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    
    @router.get("/get_shipment/{shipment_id}")
    def get_shipment(shipment_id: str):
        try:
            shipment_data = db.shipments.find_one({"_id": ObjectId(shipment_id)})
            if shipment_data:
                shipment_data["_id"] = str(shipment_data["_id"])
                return shipment_data
            else:
                raise HTTPException(status_code=404, detail="Shipment not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    return router
