import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base

from ..config import THEME_OPTIONS, AUTH_PROVIDER_OPTIONS




class Users(Base):
    __table__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email: Mapped[str] = mapped_column(String(250), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(250), nullable=False)
    business_name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    profile_image: Mapped[str] = mapped_column(String(250), default="")

    is_trial_used: Mapped[str] = mapped_column(Boolean, default=False)
    
    provider: Mapped[AUTH_PROVIDER_OPTIONS] = mapped_column(Enum(AUTH_PROVIDER_OPTIONS), default=AUTH_PROVIDER_OPTIONS.credentials_provider, nullable=True)
    provider_account_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    access_token: Mapped[str | None] = mapped_column(String, nullable=True, default="")
    refresh_token: Mapped[str | None] = mapped_column(String, nullable=True, default="")
    token_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Appearance
    theme: Mapped[THEME_OPTIONS] = mapped_column(
        Enum(THEME_OPTIONS), default=THEME_OPTIONS.dark
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relations ships
    apps: Mapped[list["App"]] = relationship(
        "App", back_populates="user", cascade="all, delete-orphan"
    )
    notifications: Mapped[list["Notification"]] = relationship(
        "Notification", back_populates="user", cascade="all, delete-orphan"
    )
    admin_feedbacks: Mapped[list["AdminFeedback"]] = relationship(
        "AdminFeedback", back_populates="user", cascade="all, delete-orphan"
    )
    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    subscriptions: Mapped[list["Subscription"]] = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) ->str:
        return f"<User id={self.id} email={self.email} >"