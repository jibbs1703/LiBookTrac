"""Pydantic Classes for the User Models"""

import re
import uuid
from datetime import date, datetime
from enum import Enum

from beanie import Document
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserType(Enum):
    student = "student"
    admin = "admin"
    staff = "staff"
    parent = "parent"


class Membership(Enum):
    active = "active"
    inactive = "inactive"


class UserRegister(BaseModel):
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

    @field_validator("first_name", "last_name", mode="before")
    @classmethod
    def convert_to_camel_case(cls, v):
        def to_camel_case(name):
            return ''.join(word.capitalize() for word in name.split())
        return to_camel_case(v)
    
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


class UserDetails(Document, UserRegister):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Unique user identifier")
    membership_status: Membership = Field(default=Membership.inactive,
                                          description="User's membership status (active/inactive)")
    membership_start_date: date | None = Field(default=None,
                                               description="Date when membership started")
    membership_end_date: date | None = Field(default=None,
                                             description="Date when membership expires")
    date_joined: date = Field(default_factory=date.today, description="Date the user registered")
    books_borrowed: int = Field(default=0, ge=0,
                                description="Number of books currently borrowed")
    max_borrow_limit: int = Field(default=5, ge=1,
                                  description="Maximum number of books a user can borrow at once")
    borrow_history: list[uuid.UUID] = Field(default_factory=list,
                                            description="List of book IDs borrowed by the user")
    fines_owed: float = Field(default=0.0, ge=0.0,
                              description="Total amount of fines owed by the user")
    is_active: bool = Field(default=True, description="Whether the user account is active")
    last_login: datetime | None = Field(default=None,
                                        description="Timestamp of the user's last login")
    password_reset_token: str | None = Field(default=None, description="Token for password reset")
    password_reset_token_expiry: datetime | None = Field(default=None,
                                                         description=(
                                                    "Expiration time for the password reset token"
                                                         ))
    preferred_genres: list[str] = Field(
        default_factory=list,
        description="User's preferred book genres"
    )
    communication_preferences: dict = Field(
        default_factory=dict,
        description=(
            "User's communication preferences (e.g., email, SMS)"
        )
    )
    parent_guardian_first_name: str | None = Field(default=None,
                                             description="First Name of the parent or guardian")
    parent_guardian_last_name: str | None = Field(default=None,
                                             description="Last Name of the parent or guardian")
    parent_guardian_contact: str | None = Field(default=None,
                                    description="Contact information for the parent or guardian")
    
    @field_validator("parent_guardian_first_name", 
                     "parent_guardian_last_name", mode="before")
    @classmethod
    def convert_to_camel_case(cls, v):
        def to_camel_case(name):
            return ''.join(word.capitalize() for word in name.split())
        return to_camel_case(v)
    
    class Settings:
        name = "users"  # MongoDB collection name
        

class UserPasswordUpdate(BaseModel):
    password: str = Field(..., min_length=8, max_length=100,
                          description="update user password")
    salt: str
