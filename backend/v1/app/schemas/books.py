"""Books Table Schema."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from sqlmodel import Field, SQLModel


class CirculationStatus(Enum):
    AVAILABLE = "available"
    CHECKED_OUT = "checked_out"
    RESERVED = "reserved"
    ON_HOLD = "on_hold"
    DAMAGED = "damaged"
    LOST = "lost"
    ARCHIVED = "archived"


class Books(SQLModel):
    uuid: UUID 
    last_updated_date: datetime
    stock_quantity: int = Field(ge=0)
