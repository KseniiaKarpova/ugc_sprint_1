from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Base0rjsonModel(BaseModel):
    class Config:
        from_attributes = True


class UserAction(Base0rjsonModel):
    action: str
    user_id: UUID
    film_id: UUID
    created_at: datetime
