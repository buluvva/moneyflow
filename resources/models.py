from pydantic import BaseModel
from datetime import datetime
from aiogram.dispatcher.filters.state import State, StatesGroup


class User(BaseModel):
    tg_user_id: str
    date_joined: datetime
    has_table: bool

    def dict(self, **kwargs):
        return super().dict(**kwargs)


class Bills(StatesGroup):
    waiting_for_category = State()
    waiting_for_move = State()
    waiting_for_value = State()
    start = State()




