from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class UserAction(BaseModel):
    action: str
    user_id: str
    film_id: str
    created_at: datetime
