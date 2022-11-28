from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    tg_user_id: str
    date_joined: datetime
    has_table: bool

    def dict(self, **kwargs):
        return super().dict(**kwargs)




