"""Pydantic Classes for the User Models"""

import re
import uuid
from datetime import date
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserType(Enum):
    student = "student"
    admin = "admin"
    staff = "staff"
    parent = "parent"


class Membership(Enum):
    active = "active"
    inactive = "inactive"


class UserBase(BaseModel):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Unique user identifier")
    first_name: str = Field(..., min_length=1, max_length=50, description="User's first name")
    last_name: str = Field(..., min_length=1, max_length=50, description="User's last name")
    phone_number: str = Field(..., pattern=r'^\d{3}-\d{3}-\d{4}$',
                              description="Phone number in USA format (e.g., 123-456-7890")
    date_of_birth: date = Field(..., description="Date of birth in MM-DD-YY")
    address: str = Field(..., min_length=5, max_length=200, description="User's full address")
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., min_length=3, max_length=30, description="Unique username for login")
    password: str = Field(..., min_length=8, max_length=100, description="User password")
    user_category: UserType
    
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        pattern = r'^\d{3}-\d{3}-\d{4}$'
        if not re.match(pattern, v):
            raise ValueError("Phone number must be in valid USA format (e.g., 123-456-7890")
        digits = re.sub(r"\D", "", v)  # Remove non-digits
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, v):
        # Ensure date of birth is in the past and user is at least 13
        today = date.today()
        age = (today - v).days // 365
        if v >= today:
            raise ValueError("Date of birth must be in the past")
        if age < 13:
            raise ValueError("User must be at least 13 years old")
        return v
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError("Username must contain only alphanumeric characters")
        return v.lower()
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        # Ensure the password meets the specified criteria
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'[!@#$%^&+*(),.?":{}|<>]', value):
            raise ValueError("Password must contain at least one special character")
        return value

    class ConfigDict:
        from_attributes = True  
