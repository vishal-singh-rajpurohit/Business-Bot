import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer, DateTime, func, Enum, Boolean, ForeignKey
from app.db.database import Base


class Apps(Base):
    __table__ = "apps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete="CASCADE"), default=uuid.uuid4)

    app_name: Mapped[str] = mapped_column(String(50), nullable=False)
    business_name: Mapped[str] = mapped_column(String(50), nullable=False)

    is_deployed: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    documents: Mapped[list["Document"]] = relationship(
        "Document", back_populates="app", cascade="all, delete-orphan"
    )
    api_keys: Mapped[list["ApiKey"]] = relationship(
        "ApiKey", back_populates="app", cascade="all, delete-orphan"
    )
    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation", back_populates="app", cascade="all, delete-orphan"
    )
    admin_feedbacks: Mapped[list["AdminFeedback"]] = relationship(
        "AdminFeedback", back_populates="app", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<App id={self.id} app_name={self.app_name} >"