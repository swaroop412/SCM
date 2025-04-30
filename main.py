
from fastapi import FastAPI
from auth.routes import auth_router,shipment_router
from pymongo import MongoClient
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app =FastAPI()

app.mount("/frontend",StaticFiles(directory="frontend"),name="frontend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



MONGODB_URI = "mongodb+srv://pswaroop412:manGO43@cluster0.dfdoi6w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGODB_URI)
db = client["user_db"]
shipment_db = client["shipment_db"]


app.include_router(auth_router(db),prefix="/auth")
app.include_router(shipment_router(shipment_db), prefix="/shipment")


