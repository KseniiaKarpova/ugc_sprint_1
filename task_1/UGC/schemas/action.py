from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class UserAction(BaseModel):
    action: str
    user_id: UUID
    film_id: UUID
    created_at: datetime = Field(default=datetime.utcnow())
