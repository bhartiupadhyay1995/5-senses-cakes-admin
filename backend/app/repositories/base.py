"""Base repository with common CRUD operations"""

from typing import Any, Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base repository class with common CRUD operations"""

    def __init__(self, session: Session, model_class: Type[ModelType]):
        self.session = session
        self.model_class = model_class

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        """Create a new instance"""
        db_obj = self.model_class(**obj_in.model_dump())
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def get(self, id: Any) -> Optional[ModelType]:
        """Get instance by ID"""
        return self.session.query(self.model_class).filter(self.model_class.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all instances with pagination"""
        return self.session.query(self.model_class).offset(skip).limit(limit).all()

    def update(self, id: Any, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        """Update an instance"""
        db_obj = self.get(id)
        if not db_obj:
            return None
        
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def delete(self, id: Any) -> Optional[ModelType]:
        """Delete an instance"""
        db_obj = self.get(id)
        if not db_obj:
            return None
        
        self.session.delete(db_obj)
        self.session.commit()
        return db_obj
