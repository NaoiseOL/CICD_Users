from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey


class Base(DeclarativeBase):
    pass

class UserDB(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    surname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    phoneNo: Mapped[str] = mapped_column(unique=True, nullable=False)

class BookingsDB(Base):
    __tablename__ = "bookings"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    surname: Mapped[str] = mapped_column(String(100), nullable=False)
    start_Date: Mapped[str] = mapped_column(String(100), nullable=False)
    end_Date: Mapped[str] = mapped_column(String(100), nullable=False)

class PaymentsDB(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(primary_key=True)
    card_no: Mapped[str] = mapped_column(String(100), nullable=False)
    expiry: Mapped[str] = mapped_column(String(100), nullable=False)
    nameOnCard: Mapped[str] = mapped_column(String(100), nullable=False)
    CVV: Mapped[str] = mapped_column(String(100), nullable=False)
    billing_address: Mapped[str] = mapped_column(String(100), nullable=False)