import uuid
import enum
from datetime import datetime

from sqlalchemy import String, Integer, Numeric, Boolean, DateTime, ForeignKey, Enum as SQLEnum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


# ---------- Enums ----------

class CouponType(str, enum.Enum):
    discount = "Discount"
    free = "Free"

class ActivationStatus(str, enum.Enum):
    active = "ACTIVE"
    expired = "EXPIRED"
    upcoming = "UPCOMING"

class PaymentStatus(str, enum.Enum):
    created = "created"
    authorized = "authorized"
    captured = "captured"
    failed = "failed"
    refunded = "refunded"


# ---------- Offer ----------

class Offer(Base):
    __tablename__ = "offers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)  # Numeric, not Float, for currency
    validity_time: Mapped[int] = mapped_column(Integer, nullable=False)   # days
    apps_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    query_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    coupons: Mapped[list["Coupons"]] = relationship("Coupons", back_populates="offer", cascade="all, delete-orphan")
    subscriptions: Mapped[list["Subscription"]] = relationship("Subscription", back_populates="offer")

    def __repr__(self) -> str:
        return f"<Offer id={self.id} title={self.title}>"


# ---------- Coupons ----------

class Coupons(Base):
    __tablename__ = "coupons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    offer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("offers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)  # added: coupons need a redeemable code
    coupon_type: Mapped[CouponType] = mapped_column(SQLEnum(CouponType, name="coupon_type_enum"), nullable=False)
    discount_percent: Mapped[int | None] = mapped_column(Integer, nullable=True)  # added: needed when coupon_type == discount
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    expires_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    offer: Mapped["Offer"] = relationship("Offer", back_populates="coupons")
    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="coupon")

    def __repr__(self) -> str:
        return f"<Coupons id={self.id} code={self.code}>"


# ---------- Payment (Razorpay-fitted) ----------

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    coupon_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("coupons.id", ondelete="SET NULL"), nullable=True, index=True
    )

    # --- Razorpay identifiers (replace generic transaction_id/transaction_id duplicate) ---
    razorpay_order_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    razorpay_payment_id: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True, index=True)
    razorpay_signature: Mapped[str | None] = mapped_column(String(255), nullable=True)  # for webhook/checkout signature verification

    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)  # store in rupees (Decimal), or store paise as Integer if you prefer Razorpay's native unit
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)  # added: Razorpay is multi-currency capable
    status: Mapped[PaymentStatus] = mapped_column(
        SQLEnum(PaymentStatus, name="payment_status_enum"), default=PaymentStatus.created, nullable=False
    )
    method: Mapped[str | None] = mapped_column(String(50), nullable=True)  # added: "card", "upi", "netbanking", etc. from Razorpay payment object

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="payments")
    coupon: Mapped["Coupons | None"] = relationship("Coupons", back_populates="payments")
    subscription: Mapped["Subscription"] = relationship("Subscription", back_populates="payment", uselist=False)

    def __repr__(self) -> str:
        return f"<Payment id={self.id} status={self.status}>"


# ---------- Subscription ----------

class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    offer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("offers.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    payment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("payments.id", ondelete="RESTRICT"), nullable=False, unique=True, index=True
    )
    activation_status: Mapped[ActivationStatus] = mapped_column(
        SQLEnum(ActivationStatus, name="activation_status_enum"), default=ActivationStatus.upcoming, nullable=False
    )
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)  # added: needed to compute expiry from offer.validity_time
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)  # added

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="subscriptions")
    offer: Mapped["Offer"] = relationship("Offer", back_populates="subscriptions")
    payment: Mapped["Payment"] = relationship("Payment", back_populates="subscription")

    def __repr__(self) -> str:
        return f"<Subscription id={self.id} status={self.activation_status}>"