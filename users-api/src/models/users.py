from uuid import UUID, uuid4
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    firstName: str
    lastName: str
    birthday: date

    @field_validator("firstName", "lastName")
    def name_must_not_be_empty_and_letters(cls, v, field):
    #Check if the string is empty or only whitespace 
        if not v or not v.strip():
            raise ValueError(f"{field.name} cannot be empty")
    #Check if all characters are
        if not v.isalpha():
            raise ValueError(f"{field.name} must contain only letters")
        return v

# Singleton UserService
class UserService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.users = []  # In-memory storage
        return cls._instance

    def create_user(self, user: User) -> User:
        self.users.append(user)
        return user

    def get_users(self) -> List[User]:
        return self.users

    def get_user(self, user_id: UUID) -> Optional[User]:
        return next((u for u in self.users if u.id == user_id), None)

    def update_user(self, user_id: UUID, updated_user: User) -> Optional[User]:
        for idx, u in enumerate(self.users):
            if u.id == user_id:
                self.users[idx] = updated_user
                return updated_user
        return None

    def delete_user(self, user_id: UUID) -> bool:
        for idx, u in enumerate(self.users):
            if u.id == user_id:
                return self.users.pop(idx)
        return None

# Dependency injection
def get_user_service() -> UserService:
    return UserService()

