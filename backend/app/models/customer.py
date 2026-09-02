from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Customer(BaseModel):
    """Customer model"""
    __tablename__ = "customers"
    
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), index=True)
    phone = Column(String(20))
    address = Column(Text)
    notes = Column(Text)  # dietary restrictions, preferences
    
    # Relationships
    orders = relationship("Order", back_populates="customer")
