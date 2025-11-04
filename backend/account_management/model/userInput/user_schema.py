# app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID


class UserCreate(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: EmailStr
    password: str
    phone: str
    address: str
    city: Optional[str] = None
    state: Optional[str] = None
    country: str
    role_id: UUID                         # FK reference to Roles table
    created_by: Optional[UUID] = None     # FK reference to Users table (creator)
