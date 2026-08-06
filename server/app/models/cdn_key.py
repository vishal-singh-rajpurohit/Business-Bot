import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.database import Base


class CDNKey(Base):
    __tablename__ = "cdn_keys"

    id: Mapped[uuid.UUID] = mapped_column(uuid.UUID(as_uuid=True), primary_key=True, index=True, autoincrement=True)
    app_id: Mapped[uuid.UUID] = mapped_column(uuid.UUID(as_uuid=True), ForeignKey("apps.id", ondelete="CASCADE"), index=True, nullable=False)

    key_name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    key_value: Mapped[str] = mapped_column(String(255), nullable=False)

    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata: Mapped[dict] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<CDNKey id={self.id} name={self.key_name}>"