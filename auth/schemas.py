from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from typing import List
from datetime import date

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    role : str

class Login(BaseModel):
    email: EmailStr
    password: str


class Shipment(BaseModel):
    user_id: int
    shipment_number: int
    container_number: int
    route_details: str
    goods_type: str
    device: str
    expected_delivery_date: date
    po_number: int
    delivery_number: int
    ndc_number: int
    batch_id: int
    serial_number_of_goods: int
    shipment_description: str


