import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.database import Base

class App(Base):
    __tablename__ = "apps"

    id: Mapped[uuid.UUID] = mapped_column(uuid.UUID(as_uuid=True),primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(uuid.UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    app_name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    business_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<App id={self.id} name={self.name}>"