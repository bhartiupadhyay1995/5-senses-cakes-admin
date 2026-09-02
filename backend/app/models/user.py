from sqlalchemy import Column, Numeric, String

from app.models.base import BaseModel


class User(BaseModel):
    """User model - Single user for the business owner"""
    __tablename__ = "users"
    
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hourly_rate = Column(Numeric(10, 2), default=20.00, nullable=False)
