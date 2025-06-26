from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    telegram_id: int = Field(index=True, unique=True)
    clients: List["Client"] = Relationship(back_populates="user")
    offer: Optional[str] = Field(default=None) # УТП


class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_username: str
    user_id: int = Field(foreign_key="user.id")
    offer_sent: bool = Field(default=False)  # Флаг, отправлено ли УТП клиенту
    user: Optional[User] = Relationship(back_populates="clients") 
