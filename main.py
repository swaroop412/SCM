import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from auth.routes import auth_router,shipment_router, device_router
from pymongo import MongoClient
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

load_dotenv()

app =FastAPI()


MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)

db = client["user_db"]
shipment_db = client["shipment_db"]
device_db = client["iot_data"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/frontend",StaticFiles(directory="frontend"),name="frontend")


@app.get("/")
async def redirect_to_frontend():
    return RedirectResponse(url="/frontend/index.html", status_code=302)

@asynccontextmanager
async def lifespan(app):
    device_db["sensor_readings"].delete_many({})
    yield

app.include_router(auth_router(db),prefix="/auth")
app.include_router(shipment_router(shipment_db), prefix="/shipment")
app.include_router(device_router(device_db))