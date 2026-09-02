"""Core domain API routes"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db_session
from app.api.errors import EntityAlreadyExistsError, EntityNotFoundError
from app.repositories import RepositoryFactory, get_repository_factory
from app.schemas.core import (
    CustomerCreate,
    CustomerListResponse,
    CustomerResponse,
    CustomerUpdate,
    UserCreate,
    UserResponse,
    UserUpdate,
)

router = APIRouter()


# ============= User Endpoints =============

@router.get("/users", response_model=List[UserResponse])
def list_users(
    session: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
):
    """List all users"""
    repos = get_repository_factory(session)
    return repos.users.get_all(skip=skip, limit=limit)


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    session: Session = Depends(get_db_session),
):
    """Create a new user"""
    repos = get_repository_factory(session)
    
    # Check if user with email already exists
    existing = repos.users.get_by_email(user_in.email)
    if existing:
        raise EntityAlreadyExistsError("User", "email", user_in.email)
    
    return repos.users.create(user_in)


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    session: Session = Depends(get_db_session),
):
    """Get a specific user"""
    repos = get_repository_factory(session)
    user = repos.users.get(user_id)
    if not user:
        raise EntityNotFoundError("User", user_id)
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_db_session),
):
    """Update a user"""
    repos = get_repository_factory(session)
    
    user = repos.users.get(user_id)
    if not user:
        raise EntityNotFoundError("User", user_id)
    
    # Check if new email already exists (if email is being updated)
    if user_update.email and user_update.email != user.email:
        existing = repos.users.get_by_email(user_update.email)
        if existing:
            raise EntityAlreadyExistsError("User", "email", user_update.email)
    
    return repos.users.update(user_id, user_update)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    session: Session = Depends(get_db_session),
):
    """Delete a user"""
    repos = get_repository_factory(session)
    
    user = repos.users.get(user_id)
    if not user:
        raise EntityNotFoundError("User", user_id)
    
    repos.users.delete(user_id)


# ============= Customer Endpoints =============

@router.get("/customers", response_model=List[CustomerListResponse])
def list_customers(
    session: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
    name: str = None,
):
    """List all customers"""
    repos = get_repository_factory(session)
    
    if name:
        return repos.customers.get_by_name(name)
    
    return repos.customers.get_all(skip=skip, limit=limit)


@router.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer_in: CustomerCreate,
    session: Session = Depends(get_db_session),
):
    """Create a new customer"""
    repos = get_repository_factory(session)
    
    # Check if customer with email already exists (if email provided)
    if customer_in.email:
        existing = repos.customers.get_by_email(customer_in.email)
        if existing:
            raise EntityAlreadyExistsError("Customer", "email", customer_in.email)
    
    return repos.customers.create(customer_in)


@router.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    session: Session = Depends(get_db_session),
):
    """Get a specific customer"""
    repos = get_repository_factory(session)
    customer = repos.customers.get(customer_id)
    if not customer:
        raise EntityNotFoundError("Customer", customer_id)
    return customer


@router.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    session: Session = Depends(get_db_session),
):
    """Update a customer"""
    repos = get_repository_factory(session)
    
    customer = repos.customers.get(customer_id)
    if not customer:
        raise EntityNotFoundError("Customer", customer_id)
    
    # Check if new email already exists (if email is being updated)
    if customer_update.email and customer_update.email != customer.email:
        existing = repos.customers.get_by_email(customer_update.email)
        if existing:
            raise EntityAlreadyExistsError("Customer", "email", customer_update.email)
    
    return repos.customers.update(customer_id, customer_update)


@router.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: int,
    session: Session = Depends(get_db_session),
):
    """Delete a customer"""
    repos = get_repository_factory(session)
    
    customer = repos.customers.get(customer_id)
    if not customer:
        raise EntityNotFoundError("Customer", customer_id)
    
    repos.customers.delete(customer_id)
