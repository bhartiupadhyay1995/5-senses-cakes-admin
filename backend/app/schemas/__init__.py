"""Core domain schemas"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema"""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    hourly_rate: float = Field(default=20.00, ge=0)


class UserCreate(UserBase):
    """User creation schema"""
    pass


class UserUpdate(BaseModel):
    """User update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    hourly_rate: Optional[float] = Field(None, ge=0)


class UserResponse(UserBase):
    """User response schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CustomerBase(BaseModel):
    """Base customer schema"""
    name: str = Field(..., min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    notes: Optional[str] = None


class CustomerCreate(CustomerBase):
    """Customer creation schema"""
    pass


class CustomerUpdate(BaseModel):
    """Customer update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    notes: Optional[str] = None


class CustomerResponse(CustomerBase):
    """Customer response schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CustomerListResponse(BaseModel):
    """Customer list response schema"""
    id: int
    name: str
    email: Optional[str]
    phone: Optional[str]

    class Config:
        from_attributes = True
