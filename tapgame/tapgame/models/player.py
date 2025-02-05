from datetime import datetime

from sqlmodel import Field, SQLModel


class Player(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    dt: datetime
    name: str
    score: int
    