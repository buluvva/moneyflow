from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    # id: int
    tg_user_id: str
    date_joined: datetime
    has_table: bool




