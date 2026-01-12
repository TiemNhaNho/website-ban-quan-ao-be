from app.models.base_model import BaseModel
from sqlalchemy import Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, declared_attr
from datetime import datetime
import enum

class Customer(BaseModel):
    def __init__(self, username, email, password_hash) -> None:
        self.username = username
        self.email = email
        self.password_hash = password_hash
    
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return "customers"
    
    class Role(str, enum.Enum):
        ADMIN = "admin"
        CUSTOMER = "customer"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(length=100), index=True)
    email: Mapped[str] = mapped_column(String(length=100), index=True)
    password_hash: Mapped[str] = mapped_column(String(length=255))
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.CUSTOMER)
    created_at: Mapped[datetime] = mapped_column(DateTime, index=True, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    is_deactivated: Mapped[bool] = mapped_column(Boolean, default=True)
    phone_number: Mapped[str | None] = mapped_column(String(length=10), nullable=True)
    address: Mapped[str | None] = mapped_column(String(length=255), nullable=True)