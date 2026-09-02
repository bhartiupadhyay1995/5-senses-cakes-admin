"""Core repositories"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models import Customer, User
from app.repositories.base import BaseRepository
from app.schemas.core import CustomerCreate, CustomerUpdate, UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """Repository for User entity"""

    def __init__(self, session: Session):
        super().__init__(session, User)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.session.query(self.model_class).filter(User.email == email).first()


class CustomerRepository(BaseRepository[Customer, CustomerCreate, CustomerUpdate]):
    """Repository for Customer entity"""

    def __init__(self, session: Session):
        super().__init__(session, Customer)

    def get_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email"""
        return self.session.query(self.model_class).filter(Customer.email == email).first()

    def get_by_name(self, name: str):
        """Get customers by name (partial match)"""
        return self.session.query(self.model_class).filter(
            Customer.name.ilike(f"%{name}%")
        ).all()
