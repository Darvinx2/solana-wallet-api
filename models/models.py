from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(primary_key=False)
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    farm: Mapped[list["Farm"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Wallet(db.Model):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(primary_key=True)
    farm_id: Mapped[int] = mapped_column(ForeignKey("farms.id"), nullable=False)
    address: Mapped[str] = mapped_column(primary_key=False)
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    farms: Mapped["Farm"] = relationship(back_populates="wallet")


class Farm(db.Model):
    __tablename__ = "farms"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    total_usd: Mapped[Decimal] = mapped_column(db.Numeric(18, 2), primary_key=False)
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    wallet: Mapped[list["Wallet"]] = relationship(
        back_populates="farms", cascade="all, delete-orphan"
    )
    user: Mapped["User"] = relationship(back_populates="farm")
