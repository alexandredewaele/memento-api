from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from app.models import EntryCategory


# ── User ─────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    username: str
    created_at: datetime
    class Config:
        from_attributes = True


# ── Token ─────────────────────────────────────────────────────────────────────

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Journal Entry ─────────────────────────────────────────────────────────────

class EntryCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1, max_length=5000)
    category: EntryCategory = EntryCategory.FACT
    phonetic: Optional[str] = Field(None, max_length=255)
    example: Optional[str] = Field(None, max_length=2000)
    is_favorite: bool = False

class EntryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1, max_length=5000)
    category: Optional[EntryCategory] = None
    phonetic: Optional[str] = Field(None, max_length=255)
    example: Optional[str] = Field(None, max_length=2000)
    is_favorite: Optional[bool] = None

class EntryResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    content: str
    category: EntryCategory
    phonetic: Optional[str]
    example: Optional[str]
    is_favorite: bool
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class EntryListResponse(BaseModel):
    entries: list[EntryResponse]
    total: int
    skip: int
    limit: int
