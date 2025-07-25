from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, Text, DateTime, func
from typing import Annotated
from datetime import datetime
from .database import Base

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
timestamp_ts = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now())]
unique_type = Annotated[str, mapped_column(nullable=False, unique=True)]
pw_type = Annotated[str, mapped_column(Text, nullable=False)]
bool_type = Annotated[bool, mapped_column(Boolean, nullable=False)]

class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    login: Mapped[unique_type]
    username: Mapped[str]
    hashed_password: Mapped[pw_type]
    email: Mapped[unique_type]
    is_active: Mapped[bool_type]
    created_at: Mapped[timestamp_ts]