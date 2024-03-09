from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class UserAction(BaseModel):
    action: str
    user_id: UUID
    film_id: UUID
    created_at: datetime = Field(default=datetime.utcnow())
