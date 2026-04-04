from pydantic import BaseModel, Field, validator
from datetime import datetime
from app.models import TransactionType, UserRole

# ------------------- Transaction Schemas -------------------

class TransactionBase(BaseModel):
    amount: float = Field(
        ...,
        gt=0,
        description="Transaction amount (must be positive)",
        example=500
    )
    type: TransactionType = Field(
        ...,
        description="Transaction type: income or expense",
        example="income"
    )
    category: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Category of the transaction",
        example="salary"
    )
    date: datetime = Field(
        ...,
        description="Date of the transaction (YYYY-MM-DD format)",
        example="2026-04-04T00:00:00"
    )
    notes: str | None = Field(
        None,
        max_length=200,
        description="Optional notes or description",
        example="April salary credited"
    )

    @validator("category")
    def category_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Category cannot be empty")
        return v

class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction"""
    pass

class Transaction(TransactionBase):
    id: int = Field(..., description="Unique ID of the transaction", example=1)

    class Config:
        from_attributes = True


# ------------------- User Schemas -------------------

class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=30,
        description="Unique username for the user",
        example="anurag"
    )
    role: UserRole = Field(
        ...,
        description="Role of the user: viewer, analyst, or admin",
        example="admin"
    )

class User(UserBase):
    id: int = Field(..., description="Unique ID of the user", example=1)

    class Config:
        from_attributes = True
