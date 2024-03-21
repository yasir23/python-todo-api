from datetime import date
from typing import Optional
from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str
    status: str
    due_date: date

    class Config:
        orm_mode = True


class TodoUpdate(BaseModel):
    title: Optional[str]
    status: Optional[str]
    due_date: Optional[date]
