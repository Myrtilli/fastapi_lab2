from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from src.models.users import User, UserService, get_user_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/users", response_model=List[User], description="Get all users", tags=["users"])
def get_users(service: UserService = Depends(get_user_service)):
    return service.get_users()

@router.get("/users/{user_id}", response_model=User, description="Get a user by special identifier", tags=["users"])
def get_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if not user:
        logger.error("User with id %s not found", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users", response_model=User)
def create_user(user: User, service: UserService = Depends(get_user_service)):
    return service.create_user(user)

@router.put("/users/{user_id}", response_model=User, tags=["users"])
def update_user(user_id: UUID, updated_user: User, service: UserService = Depends(get_user_service)):
    updated_user.id = user_id
    user = service.update_user(user_id, updated_user)
    if not user:
        logger.error("User with id %s not found", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}", response_model=User, tags=["users"])
def delete_user(user_id: UUID, deleted_user: User, service: UserService = Depends(get_user_service)):
    user = service.delete_user(user_id)
    if not user:
        logger.error("User with id %s not found", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    return user
