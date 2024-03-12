from datetime import datetime

from pydantic import BaseModel


class UserAction(BaseModel):
    action: str
    user_id: str
    film_id: str
    created_at: datetime
