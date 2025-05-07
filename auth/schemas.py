from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from typing import List
from datetime import date

class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    role : str

class Login(BaseModel):
    email: EmailStr
    password: str



class Shipment(BaseModel):
    user_id: str
    shipment_number: str
    container_number: str
    route_details: str
    goods_type: str
    device: str
    expected_delivery_date: date
    po_number: str
    delivery_number: str
    ndc_number: str
    batch_id: str
    serial_number_of_goods: str
    shipment_description: str
    created_by : str
