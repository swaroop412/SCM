from fastapi import APIRouter, HTTPException, Depends, Security , Form, Request
from auth.schemas import User, Login, Shipment
from auth.models import hash_password, verify_password
from auth.auth_handler import sign_jwt, decode_jwt
from pymongo.database import Database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from bson import ObjectId
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from datetime import date
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#yet to implement
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt(token)
    if "error" in payload:
        raise HTTPException(status_code=401, detail=payload["error"])
    return payload

#yet to implement
def require_role(role: str):
    def role_dependency(user: dict = Depends(get_current_user)):
        if user.get("role") != role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_dependency

def auth_router(db: Database):
    router = APIRouter()

    
    @router.post("/signup")
    async def signup(name :str= Form(...) ,email: str = Form(...), password: str = Form(...)):
        db_user = db.users.find_one({"email":email})
        if db_user:
            return HTMLResponse(
                "<h2>Email already registered. <a href='/frontend/index.html'>Please Login</a></h2>",
                status_code=401
            )
        
        role = "admin" if email.endswith("admin.com") else "user"

        user_data = {"name":name, 
                     "email":email,
                     "password":hash_password(password),
                     "role":role}
        db.users.insert_one(user_data)
        return HTMLResponse(
                "<h2>User Created succesfully. <a href='/frontend/index.html'>Please Login</a></h2>",
                status_code=401
            )

    @router.post("/api/signup")
    def api_signup(user: User):
        if db.users.find_one({"email": user.email}):
            raise HTTPException(status_code=400, detail="Email already registered")

        user_data = user.dict()
        user_data["password"] = hash_password(user.password)
        db.users.insert_one(user_data)
        return {"message": "User created successfully", "object_id": str(user_data["_id"]), "user_email":str(user_data["email"])}
    
    @router.post("/login")
    async def login(email: str = Form(...), password: str = Form(...)):
        
        db_user = db.users.find_one({"email": email})
       
        if not db_user or not verify_password(password, db_user["password"]):
            return HTMLResponse(
                "<h2>Invalid credentials. <a href='/frontend/index.html'>Try again</a></h2>",
                status_code=401
            )
        token = sign_jwt(email, db_user["role"],db_user["name"])
        response = RedirectResponse(url="/frontend/dashboard.html",status_code=302)
        
        response.set_cookie(key="token",value=token) # type: ignore
        response.set_cookie(key="user_name", value=db_user["name"]) # type: ignore
        response.set_cookie(key="user_email", value=db_user["email"]) # type: ignore
        response.set_cookie(key="user_role", value=db_user["role"]) # type: ignore

        return response
        '''
        if not db_user:
            return HTMLResponse("<script>alert('User does not exist, please sign up');</script>", status_code=401)
        if not verify_password(password, db_user["password"]):
            return HTMLResponse("<script>alert('Wrong password');</script><h2>Invalid credentials. <a href='/frontend/index.html'>Try again</a></h2>",status_code=401)
        return RedirectResponse(url="/frontend/dashboard.html", status_code=302)
         '''

    @router.post("/api/loginn")
    def api_login(user: Login):
        db_user = db.users.find_one({"email": user.email})
        if not db_user or not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return sign_jwt(user.email,db_user["role"],db_user["name"])
  
    @router.post("/renew_token")
    def renew_token(token: str=Depends(oauth2_scheme)):
        payload = decode_jwt(token)
        if "error" in payload:
            raise HTTPException(status_code=401,detail=payload["error"])
        
        user_id = payload["user_id"]
        role = payload["role"]
        name = payload["name"]
        return sign_jwt(user_id,role,name)
    
    @router.get("/logout")
    async def logout():
        response = RedirectResponse(url="/frontend/index.html", status_code=302)
        response.delete_cookie(key="token")
        response.delete_cookie(key="user_name")
        response.delete_cookie(key="user_email")
        response.delete_cookie(key="user_role")
        return response

    return router



def shipment_router(db: Database) -> APIRouter:
    router = APIRouter()

    @router.post("/create_shipment")
    def create_shipment(
        request: Request,
        shipment_number: str = Form(...),
        route_details: str = Form(...),
        device: str = Form(...),  
        po_number: str = Form(...),  
        ndc_number: str = Form(...),  
        serial_number_of_goods: str = Form(...),  
        container_number: str = Form(...),
        goods_type: str = Form(...),
        expected_delivery_date: str = Form(None),
        delivery_number: str = Form(...),
        batch_id: str = Form(...),
        shipment_description: str = Form(...)
        ):

        try:
            delivery_date = str(expected_delivery_date)
            user_email = request.cookies.get('user_email')
            if not user_email:
                raise HTTPException(status_code=401, detail="User email not found in cookies")
            shipment_data = {
            "shipment_number": shipment_number,
            "route_details": route_details,
            "device": device,  
            "po_number": po_number,  
            "ndc_number": ndc_number,  
            "serial_number_of_goods": serial_number_of_goods,  
            "container_number": container_number,
            "goods_type": goods_type,
            "expected_delivery_date": delivery_date,  
            "delivery_number": delivery_number,
            "batch_id": batch_id,
            "shipment_description": shipment_description,
            "created_by": user_email
            }
            db.shipments.insert_one(shipment_data)
            return HTMLResponse(content= f"""
                                <script>
                                    alert('Shipment added successfully');
                                    window.location.href="/frontend/new_shipment.html"
                                </script>   
            """)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        '''
        try:
            shipment_data = shipment.dict(by_alias=True)
            shipment_data["expected_delivery_date"] = shipment_data["expected_delivery_date"].isoformat()
            db.shipments.insert_one(shipment_data)
            return {"message": "Shipment created successfully", "shipment_id": str(shipment_data["_id"])}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        '''

    @router.post("/api/create_shipment")
    def api_create_shipment(shipment: Shipment):
        
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
    
    @router.get('/search_shipments')
    async def search_shipments(request:Request):
        user_email = request.cookies.get('user_email')
        if not user_email:
            raise HTTPException(status_code=401, detail="User email not found in cookies")
        try:
            shipments = list(db.shipments.find({"created_by":user_email}))
            for shipment in shipments:
                shipment["_id"] = str(shipment["_id"])
            return JSONResponse(content={"shipments":shipments})
        except Exception as e:
            raise HTTPException(status_code=500,detail=str(e))
    return router
