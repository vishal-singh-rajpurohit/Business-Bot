import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

from ..config import THEME_OPTIONS, AUTH_PROVIDER_OPTIONS




class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(uuid.UUID(as_uuid=True), primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    business_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    image: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_free: Mapped[str | None] = mapped_column(String(255), nullable=True)

    theme: Mapped[str] = mapped_column(enumerate(THEME_OPTIONS), nullable=False, default="light")

    Provider: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ProviderId: Mapped[str | None] = mapped_column(String(255), nullable=True)
    access_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
   
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name} email={self.email}>"
