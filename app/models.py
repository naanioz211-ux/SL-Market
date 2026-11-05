from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Numeric, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

class Merchant(Base):
    __tablename__ = "merchants"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    phone: Mapped[str] = mapped_column(String(40), default="")
    city: Mapped[str] = mapped_column(String(80), default="")
    shop_slug: Mapped[str] = mapped_column(String(140), unique=True, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    products = relationship("Product", back_populates="merchant", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    merchant_id: Mapped[int] = mapped_column(ForeignKey("merchants.id"), index=True)
    title: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(Text, default="")
    price: Mapped[float] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(8), default="USD")
    photo_file_id: Mapped[str] = mapped_column(String(255), default="")
    available: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    merchant = relationship("Merchant", back_populates="products")

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    merchant_id: Mapped[int] = mapped_column(ForeignKey("merchants.id"), index=True)
    customer_telegram_id: Mapped[int] = mapped_column(Integer)
    customer_name: Mapped[str] = mapped_column(String(120), default="")
    customer_phone: Mapped[str] = mapped_column(String(40), default="")
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String(30), default="new")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
