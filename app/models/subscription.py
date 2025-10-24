from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class SubscriptionCreate(BaseModel):
    email: EmailStr
    duration_days: int = 30


class SubscriptionVerify(BaseModel):
    code: str
    device_id: Optional[str] = None


class Subscription(BaseModel):
    id: Optional[int] = None
    code: str
    email: str
    device_id: Optional[str] = None
    duration_days: int
    created_at: datetime
    expires_at: datetime
    is_active: bool = True
    scans_count: int = 0

    class Config:
        from_attributes = True
