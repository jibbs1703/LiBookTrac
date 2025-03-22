"""Pydantic Classes for the User Models"""

import re
import uuid
from datetime import date

from pydantic import BaseModel, Field, field_validator


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, description="User's first name")
    last_name: str = Field(..., min_length=1, max_length=50, description="User's last name")
    phone_number: str = Field(..., description="Phone number in USA format (e.g., 123-456-7890)")
    date_of_birth: date = Field(..., description="User's date of birth")
    address: str = Field(..., min_length=5, max_length=200, description="User's full address")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        # Validate USA phone number format (e.g., 123-456-7890 or (123) 456-7890)
        pattern = r"^\(?[2-9]\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
        if not re.match(pattern, v):
            raise ValueError("Phone number must be in valid USA format (e.g., 123-456-7890)")
        # Normalize to XXX-XXX-XXXX format
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

    class Config:
        orm_mode = True  # Allows compatibility with ORMs like SQLAlchemy


# User Create model that extends UserBase
class UserCreate(UserBase):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Unique user identifier")
    username: str = Field(..., min_length=3, max_length=30, description="Unique username for login")
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="User password (should be hashed before storage)",
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError("Username must contain only alphanumeric characters")
        return v.lower()  # Normalize to lowercase


# Optional: User Response model for returning data (excluding sensitive info like password)
class UserResponse(UserBase):
    user_id: uuid.UUID
    username: str


class Config:
    orm_mode = True
